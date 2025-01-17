from fastapi import APIRouter
from models import session, Users
from random import randrange
from starlette.exceptions import HTTPException as StarletteHTTPException

router = APIRouter()


# register a new user
@router.post('/register')
def register(username: str, password: int, name: str, auth: int):
    try:
        new = Users(username=username, password=password, name=name, auth=auth)
        Users.insert(new)
        return {
            "success": True,
        }
    except:
        raise StarletteHTTPException(500, "internal Server Error")


# login route
@router.post('/login')
def login(username: str, password: int):
    try:
        query = session.query(Users).filter_by(username=username).all()
        record = [user.format() for user in query][0]
        if record['username'] == username and record['password'] == password:
            return {
                "success": True,
                "token": randrange(999999999, 1000000000000000),
                "id": record["id"],
                "name": record['name'],
                "username": record['username'],
                "password": record['password'],
                "auth": record["auth"]
            }
    except:
        raise StarletteHTTPException(401, "Unauthorized")


# to get users
@router.get('/users')
def users():
    try:
        query = session.query(Users).all()
        return {
            "users": [record.format() for record in query]
        }
    except:
        raise StarletteHTTPException(404, "Not Found")


# to modify user
@router.patch('/user')
def user(user_id: int, name: str, username: str, password: int, auth: int):
    try:
        query = session.query(Users).get(user_id)
        query.name = name
        query.username = username
        query.password = password
        query.auth = auth
        Users.update(query)
        return {
            "success": True
        }
    except:
        raise StarletteHTTPException(500, "internal Server Error")
