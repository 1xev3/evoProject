from pydantic import BaseModel, Field

from typing import List
from datetime import datetime

from ..database.models import TicketStatuses


class TicketMessageBase(BaseModel):
    '''
    База для сообщения тикета
    '''
    text: str = Field(title="Текст сообщения")
    date: datetime = Field(title="Дата отправки сообщения")

# пустой класс, так как в текущей реализации при создании тикета ничего не нужно
class TicketMessageCreate(TicketMessageBase):
    '''
    Модель для создания сообщения
    '''
    pass


class TicketMessage(TicketMessageBase):
    '''
    Модель представляющая собой сообщение в тикете
    '''
    id: int = Field(title="ID сообщения")

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    '''
    База для тикета
    '''
    caption: str = Field(title="Заголовок заявки")
    status: TicketStatuses = Field(title="Статус заявки", 
                                   default=TicketStatuses.awaiting_moderator, 
                                   description="""awaiting_user = 1\
        awaiting_moderator = 2\
        closed = 3
    """)


class TicketCreate(BaseModel):
    '''
    Модель для создания тикета
    '''
    caption: str = Field(title="Заголовок заявки")
    initial_message: str = Field(title="Начальное сообщение")
    #Возможно стоит принимать так-же status, но нам не нужно чтобы пользователь мог сам выбирать статус заявки.

class TicketUpdate(TicketBase):
    '''
    Модель для обновления тикета
    '''
    pass


class Ticket(TicketBase):
    '''
    Модель тикета
    '''
    id: int = Field(title="ID тикета")
    messages: List[TicketMessage] = Field(title="Список сообщений", default=[])

    class Config:
        from_attributes = True