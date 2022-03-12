from nntplib import NNTPPermanentError
from tkinter.messagebox import RETRY
import jwt
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel
from argon2 import PasswordHasher
import base64

from Cursor import Cursor

key = "5ffjucus0nk;12&7z47ddhcctaa.ixsn6d87;l5o"

ph = PasswordHasher()

success = None
warning = None
danger = None
primary = None

class User(BaseModel):
    password: str
    username: str


def create_tables():
    with Cursor("database.db") as c:
        c.execute("CREATE TABLE IF NOT EXISTS user (username TEXT, password TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS todos (username TEXT, todo_value TEXT, finished BOOLEAN, todoID TEXT)")


## TODOS API
def get_todos(token):
    try:
        payload = jwt.decode(token, key=key, algorithms=['HS256', ])
        with Cursor("database.db") as c:
            x = c.execute("SELECT * FROM user")
            items = [item for t in c.fetchall() for item in t]
            for row in x:
                print(items)
                print(payload)
                return row
    except Exception:
        print("Invalid Token")
        return False

    

## LOGIN API

# LOGIN
def login(user: User):
    with Cursor("database.db") as c:
        if check_user(username=user.username):
            c.execute("SELECT password FROM user WHERE username = ?", (user.username, ))
            hash = "".join(c.fetchone())
            try:
                if ph.verify(hash=hash, password=user.password):
                    jwttoken = jwt.encode(
                    {
                        "username": user.username,
                        "password": c.fetchone()
                    }, key=key)
                print("Logged In")
                return jwttoken
            except VerifyMismatchError:
                print("Wrong")
                return send_alertbox("warning", "Inkorrekte Benutzerinformationen", "Der Benutzername oder das Passwort ist inkorrekt", getIcon("warning"))
            
        else:
            print("No Player exists with this Playername")
            return send_alertbox("danger", "Inkorrekte Benutzerinformationen", "Der Benutzername oder das Passwort ist inkorrekt", getIcon("danger"))

## REGISTER
def register(username, password):
    with Cursor("database.db") as c:
        if not check_user(username=username):
            hash = ph.hash(password)
            c.execute("INSERT INTO user (username, password) VALUES (?,?)", (username, hash))
            print("Successfull in Database")
            return True
        else:
            print("Player already exists in database.")
            return False


# DELETE
def delete(jwtoken):
    try:
        payload = jwt.decode(jwtoken, key=key, algorithms=['HS256', ])
        password = payload["password"]
        return True
    except Exception:
        print("Invalid Token")
        return False
    


### TODO API


# CREATE TODO

def create_Todo(content, token):
    try:
        payload = jwt.decode(token, key=key, algorithms=['HS256', ])
        with Cursor("database.db") as c:
            # EXISTS? not -> CREATE ELSE -> REETURN MESSAGE
            c.execute("SELECT * FROM todo")
            pass
    except Exception:
        return False
def check_user(username):
    with Cursor("database.db") as c:
        c.execute("SELECT * FROM user WHERE username = ?", (username, ))
        fetch = c.fetchone()
        if fetch is None:
            return False
        else:
            return True




def createTodo(title, id):
    return f"""
    <label id="{id}">
        <input type="checkbox" name="finish" id="finish">
        <p>{title}</p>
        <span></span>
    </label>
    """

def send_alertbox(type, title, text, icon):
    return f"""
    <link rel="stylesheet" href="../assets/css/alerts.css">
    <div class="alert alert-{type}">
        <span class="icon">
            <i class="fa fa-{icon}"></i>
        </span>
    
        <div class="text">
            <strong>{title}</strong>
            <p>{text}</p>
        </div>
    
        <button class="close">
            <i class="fa fa-close"></i>
        </button>
        <script src="../assets/js/alerts.js">
    """

def getIcon(type):
    return "check" if type == "success" else "close" if type == "danger" else "exclamation-triangle" if type == "warning" else "info"



