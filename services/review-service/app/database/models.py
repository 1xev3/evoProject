# from fastapi import Depends
# from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from sqlalchemy import Column, ForeignKey, Integer, String, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, relationship, column_property

from app.database import db

class Review(db.BASE):
    __tablename__ = "review"
    __table_args__ = {'schema':  db.SCHEMA}

    id = Column(Integer, primary_key=True , autoincrement=True, index=True)
    creator_id = Column(UUID)
    product_id = Column(String(64))
    rating = Column(Integer, info={'min': 1, 'max': 5}) #need to be validated
    title = Column(String(255))
    text = Column(String(1024))

    # likes = relationship("Like", backref="review", cascade="all, delete-orphan")
    likes = relationship("Likes", back_populates="review", cascade="all, delete-orphan")

class Likes(db.BASE):
    __tablename__ = "likes"
    __table_args__ = {'schema': db.SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    creator_id = Column(UUID)

    review_id = Column(Integer, ForeignKey(f"{db.SCHEMA}.review.id"))
    review = relationship("Review", back_populates="likes")

