from fastapi import FastAPI, Depends, Header
from pydantic import BaseModel
from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import get_session
from crud import users_option


router= APIRouter()


@router.post("/user/registr")
def registration(fio: str,    nickname: str,    email: str, group_and_direction: str, session: Session= Depends(get_session)):
    return users_option.add_user(fio, nickname, email, session, group_and_direction)

@router.post("/user/login")
def authorizatrion(email: str="",    nickname: str="", session: Session= Depends(get_session)):
    return users_option.get_user_bu_authorization_data(email,nickname, session)