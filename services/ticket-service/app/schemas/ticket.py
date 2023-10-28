from pydantic import BaseModel, Field

from typing import List
from datetime import datetime
from uuid import UUID

from ..database.models import TicketStatuses


class TicketMessageBase(BaseModel):
    '''
    База для сообщения тикета
    '''
    text: str = Field(title="Текст сообщения")

# пустой класс, так как в текущей реализации при создании тикета ничего не нужно
class TicketMessageCreate(TicketMessageBase):
    '''
    Модель для создания сообщения
    '''
    user_id: UUID = Field(title="ID автора сообщения")


class TicketMessage(TicketMessageBase):
    '''
    Модель представляющая собой сообщение в тикете
    '''
    id: int = Field(title="ID сообщения")
    date: datetime = Field(title="Дата отправки сообщения")
    user_id: UUID = Field(title="ID автора сообщения")

    class Config:
        from_attributes = True

class TicketMessageUpdate(TicketMessageBase):
    '''
    Модель для обновления тикета
    '''
    pass



class TicketBase(BaseModel):
    '''
    База для тикета
    '''
    creator_id: UUID = Field(title="ID Создателя заявки")
    caption: str = Field(title="Заголовок заявки")
    status: TicketStatuses = Field(title="Статус заявки", 
                                   default=TicketStatuses.awaiting_moderator, 
                                   description="""awaiting_user = 1\
        awaiting_moderator = 2\
        closed = 3
    """)


class TicketCreate(BaseModel):
    '''
    Модель для создания заявки
    '''
    creator_id : UUID = Field(title="ID Создателя заявки")
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