import typing

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas.ticket import TicketBase, Ticket

app = FastAPI(
    version='0.0.1',
    title='Ticket service'
)

#Список со всеми пользователями. TODO - Заменить на PostgreSQL
tickets: typing.Dict[int, Ticket] = {}

@app.get("/tickets", summary='Возвращает список всех тикетов', response_model=list[Ticket])
async def get_tickets_list() -> typing.Iterable[Ticket] :
    return [ v for k,v in tickets.items() ]

@app.post("/tickets", status_code=201, response_model=Ticket,summary='Добавляет тикет в базу')
async def add_ticket(ticket: TicketBase) -> Ticket :
    result = Ticket(
        **ticket.model_dump(),
        id=len(tickets) + 1,
        status='awaiting user', #значение по умолчанию
    )
    tickets[result.id] = result
    return result

@app.get("/tickets/{ticketID}", summary='Возвращает информацию о тикете')
async def get_ticket_info(ticketID: int) -> Ticket :
    if ticketID in tickets: return tickets[ticketID]
    return JSONResponse(status_code=404, content={"message": "Not found!"})

@app.delete("/tickets/{ticketID}", summary='Удаляет тикет из базы')
async def delete_ticket(ticketID: int) -> Ticket :
    if ticketID in tickets:
        del tickets[ticketID]
        return JSONResponse(status_code=200, content={"message": "Deleted!"})
    return JSONResponse(status_code=404, content={"message": "Not found!"})

@app.put("/devices/{ticketID}", summary='Обновляет тикет')
async def update_ticket(ticketID: int, ticketbase: TicketBase) -> Ticket :
    if ticketID in tickets:
        result = Ticket(
            **ticketbase.model_dump(),
            id=ticketID,
            status='awaiting user',#значение по умолчанию
        )
        tickets[ticketID] = result
        return tickets[ticketID]
    return JSONResponse(status_code=404, content={"message": "Item not found"})