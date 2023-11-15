from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.broker import MessageBroker
from app import schemas

from fastapi.responses import JSONResponse


async def check_review_existing(session: AsyncSession, review_id: int) -> bool:
    existing_review = await session.execute( select(models.Review).where(models.Review.id == review_id) )
    if existing_review.scalar() is None:
        return False
    return True

async def get_like(session: AsyncSession, review_id: int, user_id):
    existing_like = await session.execute(
        select(models.Likes).where(
            (models.Likes.review_id == review_id) & (models.Likes.creator_id == user_id)
        )
    )
    return existing_like.scalar()
    # if existing_like.scalar() is None:
    #     return False
    # return True

async def get_likes(session: AsyncSession, review_id: int) -> list[models.Likes]:
    '''
    Get all likes from review
    '''
    if not (await check_review_existing(session, review_id)):
        return None

    query = select(models.Likes).filter_by(review_id=review_id)
    result = (await session.execute(query)).scalars().all()
    return result

async def create_like(session: AsyncSession, review_id: int, like: schemas.LikeBase) -> JSONResponse:
    '''
    Create a new review like
    '''

    if not (await check_review_existing(session, review_id)):
        return JSONResponse({"message": "Not found"}, 404)
    
    existing_like = await get_like(session, review_id, like.creator_id)
    if not (existing_like is None):
        return JSONResponse({"message": "Like already exists"}, 400)

    new_like = models.Likes(**like.model_dump())
    new_like.review_id = review_id
    session.add(new_like)
    
    await session.commit()
    return new_like

async def delete_like(session: AsyncSession, review_id: int, creator_id: UUID) -> JSONResponse:
    '''
    Create a new review like
    '''

    existing_like = await get_like(session, review_id, creator_id)
    if (existing_like is None):
        return JSONResponse({"message": "Not found"}, 404)

    await session.delete(existing_like)
    await session.commit()

    return JSONResponse({"message": "Like deleted!"}, 200)




async def create_review(session: AsyncSession, review: schemas.ReviewCreate, broker: MessageBroker) -> models.Review:
    '''
    Create a new review
    '''
    db_review = models.Review(**review.model_dump())
    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)

    broker.send_message(f"User {review.creator_id} has posted review to product {review.product_id}")

    return db_review

async def get_reviews(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Review]:
    '''
    Get all reviews
    '''
    query = select(models.Review).offset(skip).limit(limit)
    query_result = (await session.execute(query)).scalars().all()

    return query_result

async def get_review(session: AsyncSession, review_id: int) -> models.Review:
    '''
    Get a review by ID
    '''
    query = select(models.Review).filter(models.Review.id == review_id).limit(1)
    result = await session.execute(query)
    return result.scalars().one_or_none()

async def delete_review(session: AsyncSession, review_id: int) -> bool:
    '''
    Remove a review by ID
    '''
    has_review = await get_review(session, review_id)
    query = delete(models.Review).filter(models.Review.id == review_id)
    await session.execute(query)
    await session.commit()
    
    return bool(has_review)