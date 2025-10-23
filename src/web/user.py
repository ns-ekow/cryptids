import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User
from datetime import timedelta
from errors import Missing, Duplicate
import service.user as service

ACCESS_TOKEN_EXPIRE_MINUTES =30

router = APIRouter(prefix = "/user")

# this dependency makes a  post to "/user/token and returns an access token"
oauth2_dep = OAuth2PasswordBearer(tokenUrl= "token")

def unauthed():
    raise HTTPException(
        status_code=401,
        detail = "Incorrect username or password",
        headers={"WWW_Authenticate": "Bearer"},)


# this endpoint is directed to by any call that has the oath2_dep() dependency
@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # get username and password from Oauth from return access token
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data = {"sub": user.name}, expires = expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/")
def get_all()-> list[User]:
    return service.get_all()

@router.get("/{name}")
def get_one(name:str)-> User:
    try:
        return service.get_one(name)

    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg) 

@router.post("/", status_code=201)
def create(user: User) -> User:
    try: 
        return service.create(user)

    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch("/")
def modify(name:str, user: User)-> User:
    try:
        return service.modify(name, user)

    except Missing as exc:
        raise HTTPException(status_code=404, detail= exc.msg)

@router.delete("/{name}")
def delete(name: str) -> None:
    try: 
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)