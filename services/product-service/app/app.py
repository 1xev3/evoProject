from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

import logging
from typing import List, Annotated
from uuid import UUID

from . import config, crud
from .database import MongoDB, MinioClient
from .schemas import Product, ProductCreate, ProductUpdate


################
## INITIALIZE ##
################
logger = logging.getLogger("product-service")
logging.basicConfig(level=logging.INFO, 
                    format="[%(levelname)s][%(name)s][%(filename)s, line %(lineno)d]: %(message)s")

logger.info("Service configuration loading...")
cfg: config.Config = config.load_config(_env_file='.env')
logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.model_dump_json(by_alias=True, indent=4)}'
)

logger.info("Service database loading...")
MongoDB(mongo_dsn=cfg.mongo_dsn.unicode_string()) #connect to database
logger.info("Service database loaded")

logger.info("Service minio loading...")
minio = MinioClient(
    endpoint=cfg.minio_dsn,
    access_key=cfg.minio_access_key,
    secret_key=cfg.minio_secret_key
)
minio.init_bucket(cfg.minio_bucket_name)
logger.info("Service minio loaded")


app = FastAPI(
    version='0.0.1',
    title='Product service'
)


@app.get("/products", 
         summary="Returns all products",
         response_model=List[Product]
)
async def get_products(skip: int = 0, limit: int = 10):
    return crud.get_products(skip, limit)


@app.post("/products", 
         summary="Add new product",
         response_model=Product
)
async def add_product(product: ProductCreate) -> Product:
    return crud.add_product(product)


@app.get("/products/{product_id}", 
         summary="Get product by id",
)
async def get_product_uid(product_id: str):
    product = crud.get_product_by_uid(product_id)
    if product is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return product


@app.put("/products/{product_id}", 
         summary="Update product info by id",
)
async def update_product(product_id: str, product_update: ProductUpdate):
    product = crud.update_product_by_uid(product_id, product_update)
    if product is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return product


@app.delete("/products/{product_id}", 
         summary="Delete product by id",
)
async def delete_product(product_id: str):
    return crud.remove_product_by_uid(product_id, minio)


@app.get("/products/{product_id}/images/{file_uid}", 
        summary="Download image from product",
)
async def download_image(product_id: str, file_uid: UUID) -> StreamingResponse: #streaming response more stable
    return crud.download_image(product_id, minio, file_uid)


@app.post("/products/{product_id}/images", 
         summary="Add image to product",
)
async def upload_image(product_id: str, file: UploadFile):
    return await crud.upload_image(product_id, minio, file)


@app.delete("/products/{product_id}/images/{file_uid}", 
        summary="Delete image from product",
)
async def remove_image(product_id: str, file_uid: UUID) -> StreamingResponse:
    return crud.remove_image(product_id, minio, file_uid)