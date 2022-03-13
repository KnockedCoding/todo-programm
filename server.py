from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import jwt

from Cursor import Cursor

import api

from pydantic import BaseModel
from typing import AnyStr, Dict, Any


app = FastAPI(docs_url=None, redoc_url=None)





class Todo_Data(BaseModel):
    content: str
    jwtoken: str

class User_Data(BaseModel):
    username: str
    password: str

class TokenModel(BaseModel):
    jwtoken: str


######################### Todos API #########################

@app.post("/api/get_todos/")
async def _get_todos(jwtoken: TokenModel):
    return api.get_todos(jwtoken.jwtoken)
    
    

@app.get("/api/todos")
async def _update_todo(id, jwtoken: str):
    pass

@app.put("/api/add_todo")#########
async def _create_todo(data: Todo_Data):
    data2 = api.create_Todo(data.content, data.jwtoken)
    if data2 == False:
        return RedirectResponse("/login/")
    else:
        return data2

@app.delete("/api/todos/")
async def _delete_todo(id, jwtoken):
    pass

####################### Users API #######################

@app.get("/api/get_user/")
async def _get_user(jwtoken: str):
    pass

@app.post("/api/login/")
def _login(user: User_Data):
    return api.login(user=user)

@app.put("/api/create_user/")
async def _create_user(user: User_Data):
    with Cursor("database.db") as c:
        x = c.execute("SELECT * FROM user")
        file = open("DatabaseFile.txt", "w")
        for row in x:
            row = str(row)
            file.write("\n%s\n" % row)
            print("\n%s\n" % row)
    return api.register(user.username, user.password)

@app.post("/api/del_acc/")
async def _del_acc(token: TokenModel):
    print(token.jwtoken)
    api.delete(token.jwtoken)





@app.get("/")
async def root():
    return RedirectResponse("/index.html")


@app.get("/login/")
async def _root():
    return RedirectResponse("/login/index.html")





app.mount("/", StaticFiles(directory="www"), name="www")

uvicorn.run(app, host="0.0.0.0", port=8801)