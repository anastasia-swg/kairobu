from database import get_session
from models import (
     Event, Media
)


# EVENT
def add_event(event_date, guests_recommendet, description=None):
    session = get_session()
    obj = Event(date=event_date, description=description,  guests_recommendet= guests_recommendet)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_events():
    session = get_session()
    result = session.query(Event).all()
    session.close()
    return result


def get_event_by_id(event_id):
    session = get_session()
    result = session.query(Event).get(event_id)
    session.close()
    return result


def update_event(event_id, event_date=None, description=None, guests_recomendet=None):
    session = get_session()
    obj = session.query(Event).get(event_id)
    if obj is None:
        session.close()
        return None
    if event_date is not None:
        obj.date = event_date
    if description is not None:
        obj.description = description
    if guests_recomendet is not None:
            obj.guests_recomendet = guests_recomendet 
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def delete_event(event_id):
    session = get_session()
    obj = session.query(Event).get(event_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()


# MEDIA
def add_media(post_id, storage_url, media_format=None):
    session = get_session()
    obj = Media(post_id=post_id, storage_url=storage_url, format=media_format)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def get_media():
    session = get_session()
    result = session.query(Media).all()
    session.close()
    return result


def get_media_by_id(media_id):
    session = get_session()
    result = session.query(Media).get(media_id)
    session.close()
    return result


def get_media_by_post(post_id):
    session = get_session()
    result = session.query(Media).filter(Media.post_id == post_id).all()
    session.close()
    return result


def update_media(media_id, storage_url=None, media_format=None):
    session = get_session()
    obj = session.query(Media).get(media_id)
    if obj is None:
        session.close()
        return None
    if storage_url is not None:
        obj.storage_url = storage_url
    if media_format is not None:
        obj.format = media_format
    session.commit()
    session.refresh(obj)
    session.close()
    return obj


def delete_media(media_id):
    session = get_session()
    obj = session.query(Media).get(media_id)
    if obj is not None:
        session.delete(obj)
        session.commit()
    session.close()


