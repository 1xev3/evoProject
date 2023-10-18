import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    
    class Config:
        from_attributes = True

class GroupRead(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class GroupUpdate(BaseModel):
    name: str

    class Config:
        from_attributes = True    



class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str | None = None
    bio: str | None = None
    group_id: int | None = None


class UserCreate(schemas.BaseUserCreate):
    nickname: str = None
    bio: str = None
    group_id: int = None


class UserUpdate(schemas.BaseUserUpdate):
    nickname: str = None
    bio: str = None
    group_id: int | None = None