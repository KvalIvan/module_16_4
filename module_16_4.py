from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=15, description="Enter username")
    age: int = Field(ge=18, le=100, description="Enter age")


app = FastAPI()

users: List[User] = []


@app.get('/users', response_model=List[User])
async def user_list() -> list:
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def post_user(username, age) -> User:
    user_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='id not found')


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int) -> User:
    for i, u in enumerate(users):
        if u.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail='id not found')
