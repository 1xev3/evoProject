from .database import MinioClient
from .database import models as db_models
from .schemas import ProductCreate, Product, ProductUpdate

from io import BytesIO
from fastapi import UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
from uuid import UUID, uuid4
from logging import getLogger

from minio.deleteobjects import DeleteObject
from minio.error import S3Error

logger = getLogger("product-service")

def get_products(skip:int = 0, limit:int = 10) -> List[db_models.Product]:
    return db_models.Product.objects\
            .skip(skip)\
            .limit(limit)

def add_product(product: ProductCreate) -> db_models.Product:
    new_product = db_models.Product(
        **product.model_dump(),
        status = db_models.ProductStatusEnum.ACTIVE
    )
    new_product.save()
    
    return new_product

def db_to_product(product: db_models.Product) -> Product:
    return Product(
        unique_id=product.unique_id,
        product_name=product.product_name,
        description=product.description,
        status=product.status,
        images=product.images
    )

def get_product_by_uid(uid:UUID) -> Product:
    product = db_models.Product.objects(unique_id=uid).first()
    if product is None: return None
    return db_to_product(product)

def update_product_by_uid(uid:UUID, product_update: ProductUpdate) -> Product:
    product = db_models.Product.objects(unique_id=uid).first()
    if product is None: return None

    product.product_name = product_update.product_name
    product.description = product_update.description
    product.status = product_update.status

    product.save()
    return db_to_product(product)

def remove_product_by_uid(uid:UUID, minio:MinioClient):
    product = db_models.Product.objects(unique_id=uid).first()
    if product is None: return JSONResponse(status_code=404, content={"message": "Product not found"})

    minio_client = minio.get_client()
    minio_bucket = minio.get_bucket()

    if len(product.images) > 0:
        delete_objects = [DeleteObject(str(uuid)) for uuid in product.images]
        logger.info(f"Deleting image objects [{delete_objects}]")
        
        errors = minio_client.remove_objects(minio_bucket, delete_objects)
        for error in errors:
            logger.error(f"Error occurred when deleting image object {error}")


    product.delete()
    return JSONResponse(status_code=200, content={"message": "Deleted"})

async def upload_image(uid:UUID, minio:MinioClient, file: UploadFile):
    if not file.content_type.startswith("image"):
        return JSONResponse(status_code=400, content={"message": "File isnt image"})

    product = db_models.Product.objects(unique_id=uid).first()
    if product is None: return JSONResponse(status_code=404, content={"message": "Product not found"})
    
    filename = uuid4()

    client = minio.get_client()
    bucket_name = minio.get_bucket()
    data = BytesIO(await file.read())

    client.put_object(bucket_name=bucket_name, object_name=str(filename), data=data, length=len(data.getvalue()))
    product.images.append(filename)

    product.save()
    return JSONResponse(status_code=200, content={"message": "Uploaded", "filename": str(filename)})


def download_image(product_uid:UUID, minio:MinioClient, filename:UUID):
    product = db_models.Product.objects(unique_id=product_uid).first()
    if product is None: return JSONResponse(status_code=404, content={"message": "Product not found"})

    minio_client = minio.get_client()
    bucket_name = minio.get_bucket()

    try:
        file_stat = minio_client.stat_object(bucket_name, str(filename))
    except S3Error as Ex:
        return JSONResponse(status_code=404, content={"message": str(Ex.message)})

    #generator instance
    def generate():
        with minio_client.get_object(bucket_name, str(filename)) as file_data:
            while True:
                data = file_data.read(65536)  # Read in chunks of 64 KB
                if not data:
                    break
                yield data

    headers = {
        "Content-Disposition": f'attachment; filename="{str(filename)}"',
        "Content-Length": str(file_stat.size),
    }

    return StreamingResponse(
        content=generate(),
        media_type="image/png",  # Adjust the media type
        headers=headers,
    )


def remove_image(product_uid:UUID, minio:MinioClient, filename:UUID):
    product = db_models.Product.objects(unique_id=product_uid).first()
    if product is None: return JSONResponse(status_code=404, content={"message": "Product not found"})

    minio_client = minio.get_client()
    bucket_name = minio.get_bucket()

    #check if file exists
    try:
        minio_client.stat_object(bucket_name, str(filename))
    except S3Error as Ex:
        return JSONResponse(status_code=404, content={"message": str(Ex.message)})

    minio_client.remove_object(bucket_name, str(filename))
    product.images.remove(filename)
    product.save()

    return JSONResponse(status_code=200, content={"message": "Image deleted"})