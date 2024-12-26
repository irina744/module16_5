from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []




class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}", response_class=HTMLResponse)
def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})


@app.post("/user/{username}/{age}")
def create_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: Annotated[int, Path(gt=0, description='Enter user id')],
                username: Annotated[
                    str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail='User not found')


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users.pop(i)
    else:
        raise HTTPException(status_code=404, detail='User not found')
