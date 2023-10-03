import typing, logging

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from .database import DB_INITIALIZER
from .schemas import Ticket, TicketCreate, TicketUpdate
from .schemas import TicketMessage, TicketMessageCreate, TicketMessageBase

from . import functional, config

##===============##
## Инициализация ##
##===============##
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=20,
    format="%(levelname)-9s %(message)s"
)

logger.info("Configuration loading...")
cfg: config.Config = config.load_config(_env_file='.env')
logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.model_dump_json(by_alias=True, indent=4)}'
)


# Создать все начальные данные
logger.info('Database initialization...')
SessionLocal = DB_INITIALIZER.init_db(cfg.pg_dsn.unicode_string())

#Получить доступ к базе данных
def get_db() -> Session:
    db = SessionLocal()
    try: yield db
    finally: db.close()

#Создание приложения FastAPI
app = FastAPI(
    version='0.0.3',
    title='Ticket service'
)


##================##
## Методы тикетов ##
##================##

#Список всех тикетов
@app.get("/tickets", 
         summary='Возвращает список всех тикетов', 
         response_model=typing.List[Ticket]
)
async def get_tickets_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> typing.Iterable[Ticket] :
    return functional.get_tickets(db, skip, limit)


#Создание нового тикета
@app.post("/tickets", 
          response_model=Ticket,
          summary='Создаёт новый тикет'
)
async def new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)) -> Ticket :
    return functional.create_ticket(db, ticket)


#Получить тикет по ID
@app.get("/tickets/{ticketID}", 
         summary='Получить тикет по его ID'
)
async def get_ticket_info(ticketID: int, db: Session = Depends(get_db)) -> Ticket :
    ticket = functional.get_ticket_by_id(db, ticketID)
    if ticket != None:
        return ticket
    return JSONResponse(status_code=404, content={"message": "Ticket not found"})


#Удаление тикета
@app.delete("/tickets/{ticketID}", 
            summary='Удаляет тикет из базы по его ID'
)
async def delete_ticket(ticketID: int, db: Session = Depends(get_db)) -> Ticket :
    if functional.remove_ticket_by_id(db, ticketID):
        return JSONResponse(status_code=200, content={"message": "Ticket successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Ticket not found"})


#Обновление информации о тикете
@app.put("/tickets/{ticketID}", 
         summary='Обновляет тикет по его ID'
)
async def update_ticket(ticketID: int, ticketbase: TicketUpdate, db: Session = Depends(get_db)) -> Ticket :
    ticket = functional.update_ticket_by_id(db, ticketID, ticketbase)
    if ticket != None:
        return JSONResponse(status_code=200, content={"message": "Ticket successfully changed"})
    return JSONResponse(status_code=404, content={"message": "Ticket not found"})


#Получение сообщений в тикете
@app.get("/tickets/{ticketID}/messages", 
         summary='Получить все сообщения'
)
async def get_ticket_messages(ticketID: int, db: Session = Depends(get_db)) -> typing.Iterable[TicketMessage] :
    ticket = functional.get_ticket_by_id(db, ticketID)
    if ticket:
        return functional.ticket_get_messages(db, ticket)
    return JSONResponse(status_code=404, content={"message": "Ticket not found"})

#Отправка сообщения
@app.post("/tickets/{ticketID}/message", 
         summary='Отправить сообщение'
)
async def send_ticket_message(ticketID: int, ticket_message: TicketMessageCreate, db: Session = Depends(get_db)) -> TicketMessage:
    ticket = functional.get_ticket_by_id(db, ticketID)
    if ticket != None:
        msg = functional.ticket_send_message(db, ticket, ticket_message)
        if msg != None:
            return msg
        return JSONResponse(status_code=500, content={"message": "Message not created"})
    return JSONResponse(status_code=404, content={"message": "Ticket not found"})



##==================##
## Методы сообщений ##
##==================##

#Получение сообщения по ID
@app.get("/message/{messageID}", 
         summary='Получить сообщение по id',
         response_model=TicketMessage,
)
async def get_message_by_id(messageID: int, db: Session = Depends(get_db)) -> TicketMessage :
    message = functional.get_message_by_id(db, messageID)
    if message != None:
        return message
    return JSONResponse(status_code=404, content={"message": "Message not found"})

#Обновление информации о сообщении
@app.put("/message/{messageID}", 
         summary='Обновляет сообщение по его ID'
)
async def update_message(messageID: int, messagebase: TicketMessageBase, db: Session = Depends(get_db))  :
    status = functional.update_message_by_id(db, messageID, messagebase)
    if status != None:
        return JSONResponse(status_code=200, content={"message": "Message successfully changed"})
    return JSONResponse(status_code=404, content={"message": "Message not found"})

#Удаление сообщения
@app.delete("/message/{messageID}", 
            summary='Удаляет тикет из базы по его ID'
)
async def delete_message(messageID: int, db: Session = Depends(get_db)) :
    if functional.remove_message_by_id(db, messageID):
        return JSONResponse(status_code=200, content={"message": "Message successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Message not found"})