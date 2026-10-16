import enum
from sqlalchemy import Column, BigInteger, Date, String, ForeignKey, DateTime, Text, Enum, UniqueConstraint, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class OrganizerRole(enum.Enum):
    VOLUNTEER = "volunteer"
    TIMEKEEPER = "timekeeper"
    CURATOR = "curator"
    ORGANIZER = "organizer"

class MediaFormat(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fio = Column(String(255), nullable=False)
    nickname = Column(String(100), unique=True, nullable=False)
    group_and_direction = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)

    organizer = relationship("Organizer", back_populates="user", uselist=False)
    guest_entries = relationship("Guest", back_populates="user")


class Guest(Base):
    __tablename__ = 'guests'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    comments = Column(Text, nullable=True)

    # Составное ограничение предотвращает повторную регистрацию одного пользователя на одно и то же мероприятие
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_user_event'),
        # гарантирует, что пара (пользователь, мероприятие) уникальна. Нельзя зарегистрироваться дважды.
    )

    user = relationship("User", back_populates="guest_entries")
    event = relationship("Event", back_populates="guests")


class Event(Base):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    guests_recommendet=Column(BigInteger,nullable=True)

    guests = relationship("Guest", back_populates="event")
    organizers = relationship("OrganizerEvent", back_populates="event")
    posts = relationship("Post", back_populates="event")


class Organizer(Base):
    __tablename__ = 'organizers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    user = relationship("User", back_populates="organizer")
    posts = relationship("Post", back_populates="organizer")
    events = relationship("OrganizerEvent", back_populates="organizer")

class OrganizerEvent(Base):
    __tablename__ = 'organizer_events'

    event_id = Column(BigInteger, ForeignKey('events.id'), primary_key=True)
    organizer_id = Column(BigInteger, ForeignKey('organizers.id'), primary_key=True)
    role = Column(Enum(OrganizerRole), nullable=False)

    event = relationship("Event", back_populates="organizers")
    organizer = relationship("Organizer", back_populates="events")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    organizer_id = Column(BigInteger, ForeignKey('organizers.id'), nullable=False)
    text = Column(Text, nullable=True)
    posted_at = Column(DateTime, nullable=False, server_default=func.now())

    event = relationship("Event", back_populates="posts")
    organizer = relationship("Organizer", back_populates="posts")
    media = relationship("Media", back_populates="post")


class Media(Base):
    __tablename__ = 'media'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    post_id = Column(BigInteger, ForeignKey('posts.id'), nullable=False)
    format = Column(Enum(MediaFormat), nullable=False)
    storage_url = Column(String(500), nullable=False)

    post = relationship("Post", back_populates="media") 