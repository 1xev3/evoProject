import typing

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas.user import UserBase, User

app = FastAPI(
    version='0.0.1',
    title='User service'
)

#Список со всеми пользователями. TODO - Заменить на PostgreSQL
users: typing.Dict[int, User] = {}

@app.get("/users", summary='Возвращает список всех пользователей', response_model=list[User])
async def get_users_list() -> typing.Iterable[User] :
    return [ v for k,v in users.items() ]

@app.post("/users", status_code=201, response_model=User,summary='Добавляет пользователя в базу')
async def add_user(user: UserBase) -> User :
    result = User(
        **user.model_dump(),
        id=len(users) + 1,
        bio="test",
    )
    users[result.id] = result
    return result

@app.get("/users/{userID}", summary='Возвращает информацию об пользователе')
async def get_device_info(userID: int) -> User :
    if userID in users: return users[userID]
    return JSONResponse(status_code=404, content={"message": "Not found!"})

@app.delete("/users/{userID}", summary='Удаляет пользователя из базы')
async def delete_device(userID: int) -> User :
    if userID in users:
        del users[userID]
        return JSONResponse(status_code=200, content={"message": "Deleted!"})
    return JSONResponse(status_code=404, content={"message": "Not found!"})

@app.put("/devices/{userID}", summary='Обновляет информацию об устройстве')
async def update_device(userID: int, device: UserBase) -> User :
    if userID in users:
        result = User(
            **device.model_dump(),
            id=userID,
            bio="",
        )
        users[userID] = result
        return users[userID]
    return JSONResponse(status_code=404, content={"message": "Item not found"})