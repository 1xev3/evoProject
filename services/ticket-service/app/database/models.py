from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Date, Enum
from typing import Literal
from sqlalchemy.orm import relationship

import enum

from .db import Base

#Список возможных статусов заявки
class TicketStatuses(enum.Enum):
    awaiting_user = 1
    awaiting_moderator = 2
    closed = 3

class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, index=True)

    creator_id = Column(Integer)
    caption = Column(String)
    status = Column(Enum(TicketStatuses), default=TicketStatuses.awaiting_moderator)

    messages = relationship("TicketMessage", back_populates="ticket") #установка отношения

class TicketMessage(Base):
    __tablename__ = "ticket_message"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)

    text = Column(String)
    date = Column(Date)

    ticket_id = Column(Integer, ForeignKey("ticket.id"))
    ticket = relationship("Ticket", back_populates="messages")