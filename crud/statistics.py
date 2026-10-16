from database import get_session
from models import (
    User, Event, Organizer, Post
)

# АНАЛИТИКА И НАВИГАЦИЯ ПО СВЯЗЯМ
def count_guests_on_event(event_id):
    session = get_session()
    event = session.query(Event).get(event_id)
    if event is None:
        session.close()
        return 0
    result = len(event.guests)
    session.close()
    return result


def count_events_by_organizer(organizer_id):
    session = get_session()
    organizer = session.query(Organizer).get(organizer_id)
    if organizer is None:
        session.close()
        return 0
    result = len(organizer.events)
    session.close()
    return result


def count_posts_on_event(event_id):
    session = get_session()
    event = session.query(Event).get(event_id)
    if event is None:
        session.close()
        return 0
    result = len(event.posts)
    session.close()
    return result


def get_user_events(user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    if user is None:
        session.close()
        return []
    result = [g.event for g in user.guest_entries]
    session.close()
    return result


def get_event_organizers(event_id):
    session = get_session()
    event = session.query(Event).get(event_id)
    if event is None:
        session.close()
        return []
    result = [
        {
            "organizer": oe.organizer,
            "user": oe.organizer.user,
            "role": oe.role
        }
        for oe in event.organizers
    ]
    session.close()
    return result


def get_post_media(post_id):
    session = get_session()
    post = session.query(Post).get(post_id)
    if post is None:
        session.close()
        return []
    result = post.media
    session.close()
    return result