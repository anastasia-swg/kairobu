from database import get_session
from sqlalchemy.orm import selectinload
from models import (    User, Guest)

def add_user(fio, nickname, email, group_and_direction=None):
    session = get_session()
    obj = User(fio=fio, nickname=nickname, email=email,
               group_and_direction=group_and_direction)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_users():
    session = get_session()
    result = session.query(User).all()
    session.close()
    return result


def get_user_by_id(user_id):
    session = get_session()
    result = session.query(User).options(selectinload(User.organizer)).get(user_id)
    session.close()
    return result


def update_user(user_id, fio=None, nickname=None, email=None, group_and_direction=None):
    session = get_session()
    obj = session.query(User).get(user_id)
    if obj is None:
        session.close()
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
    session.close()
    return obj


def delete_user(user_id):
    session = get_session()
    obj = session.query(User).get(user_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()

# GUEST
def add_guest(user_id, event_id, comments=None):
    session = get_session()
    obj = Guest(user_id=user_id, event_id=event_id, comments=comments)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_guests():
    session = get_session()
    result = session.query(Guest).all()
    session.close()
    return result


def get_guest_by_id(guest_id):
    session = get_session()
    result = session.query(Guest).get(guest_id)
    session.close()
    return result


def get_guests_by_event(event_id):
    session = get_session()
    result = session.query(Guest).filter(Guest.event_id == event_id).all()
    session.close()
    return result


def get_guests_by_user(user_id):
    session = get_session()
    result = session.query(Guest).filter(Guest.user_id == user_id).all()
    session.close()
    return result


def update_guest(guest_id, comments=None):
    session = get_session()
    obj = session.query(Guest).get(guest_id)
    if obj is None:
        session.close()
        return None
    if comments is not None:
        obj.comments = comments
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def delete_guest(guest_id):
    session = get_session()
    obj = session.query(Guest).get(guest_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()