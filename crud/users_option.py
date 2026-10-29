from database import get_session
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import (    User, Guest)

def add_user(fio, nickname, email, session: Session, group_and_direction=None):
    obj = User(fio=fio, nickname=nickname, email=email,
               group_and_direction=group_and_direction)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_users(session: Session):
    result = session.query(User).all()
    return result


def get_user_by_id(user_id, session: Session):
    result = session.query(User).options(selectinload(User.organizer)).get(user_id)
    return result

def get_user_bu_authorization_data(cur_email, cur_nikname,  session: Session):
    result= session.query(User).filter(or_(User.email== cur_email, User.nickname==cur_nikname)).first()
    return result;

def update_user(user_id,session: Session,  fio=None, nickname=None, email=None, group_and_direction=None):
    obj = session.query(User).get(user_id)
    if obj is None:
        return None
    if fio is not None:
        obj.fio = fio
    if nickname is not None:
        obj.nickname = nickname
    if email is not None:
        obj.email = email
    if group_and_direction is not None:
        obj.group_and_direction = group_and_direction
    session.commit()
    session.refresh(obj)
    return obj


def delete_user(user_id, session: Session):
    obj = session.query(User).get(user_id)
    if obj is not None:
        session.delete(obj)
        session.commit()

# GUEST
def add_guest(user_id, event_id, session: Session,  comments=None):
    obj = Guest(user_id=user_id, event_id=event_id, comments=comments)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_guests(session: Session):
    result = session.query(Guest).all()
    return result


def get_guest_by_id(guest_id, session: Session, ):
    result = session.query(Guest).get(guest_id)
    return result


def get_guests_by_event(event_id, session: Session, ):
    result = session.query(Guest).filter(Guest.event_id == event_id).all()
    return result


def get_guests_by_user(user_id, session: Session, ):
    result = session.query(Guest).filter(Guest.user_id == user_id).all()
    return result


def update_guest(guest_id,session: Session,  comments=None):
    obj = session.query(Guest).get(guest_id)
    if obj is None:
        return None
    if comments is not None:
        obj.comments = comments
    session.commit()
    session.refresh(obj)

    return obj


def delete_guest(guest_id, session: Session):
    obj = session.query(Guest).get(guest_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
