import typing

from datetime import datetime
from sqlalchemy.orm import Session

from .database import models as db_models
from . import schemas

def get_tickets(db: Session, skip:int = 0, limit:int = 100) -> typing.Iterable[db_models.Ticket]:
    '''
    Получение всех тикетов
    '''
    return db.query(db_models.Ticket) \
            .offset(skip) \
            .limit(limit) \
            .all()

def create_ticket(db: Session, ticket: schemas.TicketCreate) -> db_models.Ticket:
    '''
    Создать новый тикет
    '''

    initial_message = db_models.TicketMessage(
        text = ticket.initial_message,
        date = datetime.now()
    )

    new_ticket = db_models.Ticket(
        caption = ticket.caption,
        status = db_models.TicketStatuses.awaiting_moderator, #default value for new ticket
        messages = [],
    )
    new_ticket.messages.append(initial_message)

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

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

def update_ticket_by_id(db:Session, ticket_id: int, ticket: schemas.Ticket) -> db_models.Ticket:
    '''
    Обновить тикет по ID
    '''

    result = db.query(db_models.Ticket) \
                .filter(db_models.Ticket.id == ticket_id) \
                .update(ticket.model_dump())
    db.commit()

    if result == 1:
        return get_ticket_by_id(db, ticket_id)
    return None