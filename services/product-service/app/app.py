from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from typing import List, Union
from uuid import UUID

from . import config, crud
from .database import MongoDB
from .schemas import Product, ProductCreate, ProductUpdate




################
## INITIALIZE ##
################
cfg: config.Config = config.load_config(_env_file='.env')
MongoDB(mongo_dns = cfg.mongo_dsn.unicode_string()) #connect to database

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

@app.post("/product", 
         summary="Add new products",
         response_model=Product
)
async def add_product(product: ProductCreate) -> Product:
    return crud.add_product(product)

@app.get("/product/{product_uid}", 
         summary="Get product by uid",
)
async def get_product_uid(product_uid: UUID):
    product = crud.get_product_by_uid(product_uid)
    if product is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return product

@app.put("/product/{product_uid}", 
         summary="Update product info by uid",
)
async def update_product(product_uid: UUID, product_update: ProductUpdate):
    product = crud.update_product_by_uid(product_uid, product_update)
    if product is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return product

@app.delete("/product/{product_uid}", 
         summary="Delete product by uid",
)
async def delete_product(product_uid: UUID):
    product = crud.remove_product_by_uid(product_uid)
    if product == True:
        return JSONResponse(status_code=200, content={"message": "Deleted"})
    return JSONResponse(status_code=404, content={"message": "Not found"})
