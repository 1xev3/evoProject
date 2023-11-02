import typing

from datetime import datetime
from sqlalchemy.orm import Session

from .database import models as db_models
from . import schemas

from .broker import MessageBroker

def create_ticket_message(user_id: int, text: str):
    return db_models.TicketMessage(
        text = text,
        user_id = user_id,
        date = datetime.now(),
    )

def get_tickets(db: Session, skip:int = 0, limit:int = 100) -> typing.Iterable[db_models.Ticket]:
    '''
    Получение всех тикетов
    '''
    return db.query(db_models.Ticket) \
            .offset(skip) \
            .limit(limit) \
            .all()

def create_ticket(db: Session, broker:MessageBroker, ticket: schemas.TicketCreate) -> db_models.Ticket:
    '''
    Создать новый тикет
    '''

    #Начальное сообщение
    initial_message = create_ticket_message(ticket.creator_id, ticket.initial_message)


    new_ticket = db_models.Ticket(
        creator_id = ticket.creator_id,
        caption = ticket.caption,
        status = db_models.TicketStatuses.awaiting_moderator, #default value for new ticket
        messages = [],
    )
    new_ticket.messages.append(initial_message)

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    broker.send_message(f"New ticket has created by user {ticket.creator_id}. Caption: {ticket.caption}")

    return new_ticket

def get_ticket_by_id(db: Session, ticket_id:int) -> db_models.Ticket:
    '''
    Получить тикет по ID
    '''

    return db.query(db_models.Ticket) \
            .filter(db_models.Ticket.id == ticket_id) \
            .first()


def remove_ticket_by_id(db: Session, ticket_id:int) -> bool:
    '''
    Удалить тикет по ID
    '''
    ticket = get_ticket_by_id(db, ticket_id)

    if ticket != None:
        #Удаляем связанные сообщения
        for message in ticket.messages:
            db.delete(message)

        db.delete(ticket)

        db.commit()
        return True
    return False

def update_ticket_by_id(db:Session, ticket_id: int, ticket: schemas.TicketUpdate) -> db_models.Ticket:
    '''
    Обновить тикет по ID
    '''

    filter = db.query(db_models.Ticket).filter(db_models.Ticket.id == ticket_id) 
    result = filter.update(ticket.model_dump())
    ticket_r = filter.first()
    db.commit()

    if result == 1:
        return ticket_r
    return None

def ticket_get_messages(db:Session, ticket: db_models.Ticket) -> typing.Iterable[db_models.TicketMessage]:
    '''
    Получить все сообщения по тикету
    '''
    return ticket.messages

def ticket_send_message(db:Session, ticket: db_models.Ticket, ticket_message: schemas.TicketMessageCreate):
    '''
    Отправить новое сообщение в тикет
    '''
    new_message = create_ticket_message(ticket_message.user_id, ticket_message.text)
    ticket.messages.append(new_message)
    db.commit()

    return new_message
    
def get_message_by_id(db:Session, message_id: int):
    '''
    Получить сообщение по его ID
    '''
    return db.query(db_models.TicketMessage) \
            .filter(db_models.TicketMessage.id == message_id) \
            .first()

def update_message_by_id(db:Session, message_id: int, message: schemas.TicketMessageUpdate) -> db_models.Ticket:
    '''
    Обновить сообщение по ID
    '''
    filter = db.query(db_models.TicketMessage).filter(db_models.TicketMessage.id == message_id) 
    result = filter.update(message.model_dump())
    message = filter.first()
    db.commit()

    if result == 1:
        return message
    return None

def remove_message_by_id(db: Session, message_id:int) -> bool:
    '''
    Удалить сообщение по ID
    '''
    message = get_message_by_id(db, message_id)

    if message_id != None:
        db.delete(message)
        db.commit()
        return True
    return False