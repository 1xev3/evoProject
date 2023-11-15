from pydantic import BaseModel, Field, Base64Bytes
from typing import Optional, List, Any, Annotated
from uuid import UUID

class LikeBase(BaseModel):
    creator_id: UUID = Field(title="Like")

class Like(LikeBase):
    id: int = Field(title="Like ID")
    review_id: int = Field(title="Related review ID")

class ReviewBase(BaseModel):
    rating: int = Field(title="Review rating [1,5]", ge=1, le=5, default=5)
    product_id: str = Field(title="Product ID")
    creator_id: UUID = Field(title="Review creator UID")
    title: Optional[str] = Field(title="Review title")
    text: Optional[str] = Field(title="Review text")

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int = Field(title="Review ID")