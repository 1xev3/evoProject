import typing

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .schemas import Ticket, TicketCreate, TicketUpdate

from . import functional

##===============##
## Инициализация ##
##===============##

# Создать все начальные данные
Base.metadata.create_all(bind=engine)

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


##========##
## Методы ##
##========##

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
    return JSONResponse(status_code=404, content={"message": "Not found"})


#Удаление тикета
@app.delete("/tickets/{ticketID}", 
            summary='Удаляет тикет из базы по его ID'
)
async def delete_ticket(ticketID: int, db: Session = Depends(get_db)) -> Ticket :
    if functional.remove_ticket_by_id(db, ticketID):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Not found"})


#Обновление информации о тикете
@app.put("/tickets/{ticketID}", 
         summary='Обновляет тикет по его ID'
)
async def update_ticket(ticketID: int, ticketbase: TicketUpdate, db: Session = Depends(get_db)) -> Ticket :
    ticket = functional.update_ticket_by_id(db, ticketID, ticketbase)
    if ticket != None:
        return JSONResponse(status_code=200, content={"message": "Item successfully changed"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})