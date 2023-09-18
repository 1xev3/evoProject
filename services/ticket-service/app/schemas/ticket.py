from pydantic import BaseModel, Field
from typing import Literal

#То что требуется при первом создании
class TicketBase(BaseModel):
    caption:str = Field(title='Заголовок тикета')
    message:str = Field(title='Начальное сообщение тикета')
    
#Нам не нужно указывать ID и STATUS в первом запросе так как они заполняются автоматически
class Ticket(TicketBase):
    id: int = Field(title='Айди тикета')
    status: Literal['awaiting user', 'awaiting moderator', 'closed']