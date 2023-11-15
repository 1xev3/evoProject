import typing, logging, json
from uuid import UUID

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from . import database, config, schemas, broker, crud



##======##
## INIT ##
##======##
logger = logging.getLogger("review-service")
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

message_broker = broker.MessageBroker(
    ampq_dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name=cfg.EXCHANGE_NAME,
    queue_name=cfg.QUEUE_NAME,
)


app = FastAPI(
    version='0.0.1',
    title='Review service'
)


##=====================##
## REGISTERING METHODS ##
##=====================##
@app.post("/reviews", 
         summary="Create new review",
         response_model=schemas.Review,
         tags=["reviews"]
)
async def post_reviews(review: schemas.ReviewCreate,
        session: AsyncSession = Depends(database.get_async_session)):
    return await crud.create_review(session, review, message_broker)


@app.get("/reviews", 
         summary="Returns all reviews",
         response_model=list[schemas.Review],
         tags=["reviews"]
)
async def get_reviews(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(database.get_async_session)):
    return await crud.get_reviews(session, skip, limit)

@app.get("/reviews/{Review_ID}", 
         summary="Return review by its ID",
         response_model=schemas.Review,
         tags=["reviews"]
)
async def get_review(Review_ID: int, session: AsyncSession = Depends(database.get_async_session)):
    return await crud.get_review(session, Review_ID)

@app.delete("/reviews/{Review_ID}", 
         summary="Delete review by its ID",
         tags=["reviews"]
)
async def remove_review(Review_ID: int, session: AsyncSession = Depends(database.get_async_session)):
    result = await crud.delete_review(session, Review_ID)
    if result == True:
        return JSONResponse({"message": "Review deleted!"}, 200)
    return JSONResponse({"message": "Not found"}, 404)



@app.get("/reviews/{Review_ID}/likes", 
         summary="Return review likes by its ID",
         tags=["reviews"]
)
async def get_review_likes(Review_ID: int, session: AsyncSession = Depends(database.get_async_session)):
    result = await crud.get_likes(session, Review_ID)
    if result is None:
        return JSONResponse({"message": "Not found"}, 404)
    return result

@app.post("/reviews/{Review_ID}/likes", 
         summary="Creates review like",
         tags=["reviews"]
)
async def post_review_likes(Review_ID: int, like: schemas.LikeBase, session: AsyncSession = Depends(database.get_async_session)):
    return await crud.create_like(session, Review_ID, like)

@app.delete("/reviews/{Review_ID}/likes", 
         summary="Delete review like by UserID",
         tags=["reviews"]
)
async def post_review_likes(Review_ID: int, user_id: UUID, session: AsyncSession = Depends(database.get_async_session)):
    return await crud.delete_like(session, Review_ID, user_id)


@app.on_event("startup")
async def on_startup():
    logger.info("Database initialization...")
    await database.DB_INITIALIZER.init_db(
        cfg.pg_dsn.unicode_string()
    )
