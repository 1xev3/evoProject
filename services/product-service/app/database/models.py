from mongoengine import Document
from mongoengine import StringField, EnumField, BinaryField, ListField, UUIDField
from uuid import uuid4


from enum import Enum

class ProductStatusEnum(Enum):
    '''
    ACTIVE = 1
    IN_DEVELOPMENT = 2
    FROZEN = 3
    CLOSED = 4
    '''
    ACTIVE = 1
    IN_DEVELOPMENT = 2
    FROZEN = 3
    CLOSED = 4

# Определение модели данных
class Product(Document):
    unique_id = UUIDField(binary=False, default=uuid4, unique=True)
    product_name = StringField(required=True,max_length=60)
    description = StringField()
    status = EnumField(ProductStatusEnum, required=True)
    images = ListField(UUIDField(binary=False, unique=True))

    #nice view
    def __str__(self):
        return f"Product(product_name={self.product_name}, status={self.status})"
