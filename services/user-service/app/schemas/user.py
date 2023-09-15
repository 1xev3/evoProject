from pydantic import BaseModel, Field
from typing import Optional

#То что требуется при первом создании
class UserBase(BaseModel):
    name:str = Field(title='Никнейм пользователя')
    password:str = Field(title='Пароль пользователя')
    
class User(UserBase):
    id: int = Field(title='Идентификатор пользователя')
    bio: Optional[str] = Field(title='Биография пользователя')