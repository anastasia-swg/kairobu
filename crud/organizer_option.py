from database import get_session
from models import (
Organizer, OrganizerEvent, Post
)

# ORGANIZER
def add_organizer(user_id, description=None):
    session = get_session()
    obj = Organizer(user_id=user_id, description=description)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_organizers():
    session = get_session()
    result = session.query(Organizer).all()
    session.close()
    return result


def get_organizer_by_id(organizer_id):
    session = get_session()
    result = session.query(Organizer).get(organizer_id)
    session.close()
    return result


def get_organizer_by_user(user_id):
    session = get_session()
    result = session.query(Organizer).filter(Organizer.user_id == user_id).first()
    session.close()
    return result


def update_organizer(organizer_id, description=None):
    session = get_session()
    obj = session.query(Organizer).get(organizer_id)
    if obj is None:
        session.close()
        return None
    if description is not None:
        obj.description = description
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def delete_organizer(organizer_id):
    session = get_session()
    obj = session.query(Organizer).get(organizer_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()

    

# ORGANIZER_EVENT (M:N)
def add_organizer_event(organizer_id, event_id, role):
    session = get_session()
    obj = OrganizerEvent(
        organizer_id=organizer_id,
        event_id=event_id,
        role=role
    )
    session.add(obj)
    session.commit()
    session.close()
    return obj


def get_organizer_events():
    session = get_session()
    result = session.query(OrganizerEvent).all()
    session.close()
    return result


def get_organizer_events_by_event(event_id):
    session = get_session()
    result = session.query(OrganizerEvent).filter(
        OrganizerEvent.event_id == event_id
    ).all()
    session.close()
    return result


def get_organizer_events_by_organizer(organizer_id):
    session = get_session()
    result = session.query(OrganizerEvent).filter(
        OrganizerEvent.organizer_id == organizer_id
    ).all()
    session.close()
    return result


def update_organizer_event_role(organizer_id, event_id, role):
    session = get_session()
    obj = session.query(OrganizerEvent).get((event_id, organizer_id))
    if obj is None:
        session.close()
        return None
    obj.role = role
    session.commit()
    session.close()
    return obj


def delete_organizer_event(organizer_id, event_id):
    session = get_session()
    obj = session.query(OrganizerEvent).get((event_id, organizer_id))
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()

    
# POST
def add_post(event_id, organizer_id, text=None):
    session = get_session()
    obj = Post(event_id=event_id, organizer_id=organizer_id, text=text)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_posts():
    session = get_session()
    result = session.query(Post).all()
    session.close()
    return result


def get_post_by_id(post_id):
    session = get_session()
    result = session.query(Post).get(post_id)
    session.close()
    return result


def get_posts_by_event(event_id):
    session = get_session()
    result = session.query(Post).filter(Post.event_id == event_id).all()
    session.close()
    return result


def get_posts_by_organizer(organizer_id):
    session = get_session()
    result = session.query(Post).filter(Post.organizer_id == organizer_id).all()
    session.close()
    return result


def update_post(post_id, text=None):
    session = get_session()
    obj = session.query(Post).get(post_id)
    if obj is None:
        session.close()
        return None
    if text is not None:
        obj.text = text
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def delete_post(post_id):
    session = get_session()
    obj = session.query(Post).get(post_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()