from pydantic import BaseModel, Field, Base64Bytes
from typing import Optional, List

from ..database.models import ProductStatusEnum

from uuid import UUID
from enum import Enum


class ProductBase(BaseModel):
    product_name: str = Field(title="Product name")
    description: Optional[str] = Field(title="Product description", default="Description")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    status: ProductStatusEnum = Field(title="Product status")
    images: Optional[List[Base64Bytes]] = Field(title="Product images", default=[])

class Product(ProductBase):
    unique_id: UUID = Field(title="Unique field from database")
    status: ProductStatusEnum = Field(title="Product status")
    images: Optional[List[Base64Bytes]] = Field(title="Product images", default=[])