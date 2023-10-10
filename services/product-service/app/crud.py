from .database import models as db_models
from .schemas import ProductCreate, Product, ProductUpdate

from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID

from mongoengine import DoesNotExist


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

    print(product_update.images)
    product.product_name = product_update.product_name
    product.description = product_update.description
    product.status = product_update.status

    product.save()
    return db_to_product(product)

def remove_product_by_uid(uid:UUID) -> Product:
    product = db_models.Product.objects(unique_id=uid).first()
    if product is None: return False
    product.delete()
    return True