
from datetime import date, timedelta

from database import engine
from models import Base, OrganizerRole, MediaFormat

from crud import users_option, event, organizer_option, statistics


# ============================================================
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def reset_db():
    """Пересоздать таблицы. ТОЛЬКО для теста."""
    print(">>> Пересоздание таблиц...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print(">>> OK\n")


def section(title: str):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


def sub(title: str):
    print(f"\n--- {title} ---")


# ============================================================
#  СЦЕНАРИЙ 1: ОРГАНИЗАТОР
# ============================================================

def scenario_organizer():
    section("СЦЕНАРИЙ 1: ОРГАНИЗАТОР")

    # -------- 1. Создание User --------
    sub("1.1 Создание User (будущий организатор)")
    org_user = users_option.add_user(
        fio="Иванов Иван Иванович",
        nickname="ivan_org",
        email="ivan_org@club.ru",
        group_and_direction="ИУ7-31Б, Техническая кибернетика",
    )
    print(f"User: id={org_user.id}, nickname={org_user.nickname}, email={org_user.email}")

    # -------- 2. Идентификация: создание Organizer --------
    sub("1.2 Создание Organizer для этого User")
    org = organizer_option.add_organizer(
        user_id=org_user.id,
        description="Ответственный за музыкальное направление",
    )
    print(f"Organizer: id={org.id}, user_id={org.user_id}")

    # -------- 4. Создание Event --------
    sub("1.4 Создание Event")
    ev = event.add_event(
        event_date=date.today() + timedelta(days=30),
        description="Осенний фестиваль гик-культуры GIK FEST 2027",
        guests_recommendet=200,
    )
    print(f"Event: id={ev.id}, date={ev.date}, "
          f"guests_recommendet={ev.guests_recommendet}")
    print(f"       description={ev.description!r}")

    # -------- 5. Назначение организатора на меро --------
    sub("1.5 Назначение организатора на мероприятие")
    oe = organizer_option.add_organizer_event(
        organizer_id=org.id,
        event_id=ev.id,
        role=OrganizerRole.ORGANIZER,
    )
    print(f"OrganizerEvent: event_id={oe.event_id}, "
          f"organizer_id={oe.organizer_id}, role={oe.role.value}")

    # -------- 6. Второй организатор — проверка M:N --------
    sub("1.6 Второй организатор на то же мероприятие (M:N)")
    org_user2 = users_option.add_user(
        fio="Петрова Мария Сергеевна",
        nickname="maria_vol",
        email="maria_vol@club.ru",
        group_and_direction="ИУ7-32Б, Техническая кибернетика",
    )
    org2 = organizer_option.add_organizer(
        user_id=org_user2.id,
        description="Волонтёр",
    )
    organizer_option.add_organizer_event(
        organizer_id=org2.id,
        event_id=ev.id,
        role=OrganizerRole.VOLUNTEER,
    )
    on_event = organizer_option.get_organizer_events_by_event(ev.id)
    print(f"Организаторов на меро {ev.id}: {len(on_event)}")

    # -------- 7. Создание Post --------
    sub("1.7 Создание Post")
    post = organizer_option.add_post(
        event_id=ev.id,
        organizer_id=org.id,
        text="Открыта регистрация на фестиваль! Успейте подать заявку.",
    )
    print(f"Post: id={post.id}, event_id={post.event_id}, "
          f"organizer_id={post.organizer_id}")
    print(f"      text={post.text!r}")

    
    # -------- 8. Создание Media --------
    sub("1.8 Добавление Media к посту")
    m1 = event.add_media(
        post_id=post.id,
        storage_url="https://i.pinimg.com/736x/aa/b0/9e/aab09e760e7a878a854afd52c8ab3470.jpg",
        media_format=MediaFormat.IMAGE,
    )
    m2 = event.add_media(
        post_id=post.id,
        storage_url="https://youtu.be/dQw4w9WgXcQ?si=WmMKy_GXS60o7LF4",
        media_format=MediaFormat.VIDEO,
    )
    print(f"Media: id={m1.id} [{m1.format.value}], id={m2.id} [{m2.format.value}]")


    # -------- 9. Статистика --------
    sub("1.9 Статистика по мероприятию")
    print(f"Гостей записано:          {statistics.count_guests_on_event(ev.id)}")
    print(f"Постов на меро:           {statistics.count_posts_on_event(ev.id)}")
    print(f"Мероприятий у организатора: "
          f"{statistics.count_events_by_organizer(org.id)}")

    print("\nОрганизаторы меро:")
    for o in statistics.get_event_organizers(ev.id):
        print(f"  • {o['user'].fio} — {o['role'].value}")

    print("\nМедиа поста:")
    for m in statistics.get_post_media(post.id):
        print(f"  • [{m.format.value}] {m.storage_url}")

    return ev, org_user


# ============================================================
#  СЦЕНАРИЙ 2: ГОСТЬ
# ============================================================

def scenario_guest(existing_event_id: int):
    section("СЦЕНАРИЙ 2: ГОСТЬ")

    # -------- 1. Создание User --------
    sub("2.1 Создание User (гость)")
    guest_user = users_option.add_user(
        fio="Сидоров Алексей Петрович",
        nickname="alex_guest",
        email="alex_guest@student.ru",
        group_and_direction="ИУ7-33Б, Прикладная математика",
    )
    print(f"User: id={guest_user.id}, nickname={guest_user.nickname}")

    # -------- 2. Идентификация: гость или организатор? --------
    sub("2.2 Идентификация — организатор или гость?")
    fetched = users_option.get_user_by_id(guest_user.id)
    is_organizer = fetched.organizer is not None
    print(f"Является ли организатором: {is_organizer}")

    # -------- 3. Просмотр мероприятий --------
    sub("2.3 Просмотр всех мероприятий")
    all_events = event.get_events()
    print(f"Всего мероприятий: {len(all_events)}")
    for e in all_events:
        guests_now = statistics.count_guests_on_event(e.id)
        print(f"  • id={e.id}, date={e.date}, "
              f"рекомендовано={e.guests_recommendet}, "
              f"записано={guests_now}")

    # -------- 4. Запись на мероприятие --------
    sub("2.4 Запись на мероприятие")
    g = users_option.add_guest(
        user_id=guest_user.id,
        event_id=existing_event_id,
        comments="Буду с друзьями, нужен ранний вход",
    )
    print(f"Guest: id={g.id}, user_id={g.user_id}, "
          f"event_id={g.event_id}, comments={g.comments!r}")

    # -------- 5. Проверка записи --------
    sub("2.5 Проверка записи")
    guests_on_event = users_option.get_guests_by_event(existing_event_id)
    print(f"Гостей на меро {existing_event_id}: {len(guests_on_event)}")
    for gg in guests_on_event:
        print(f"  • guest_id={gg.id}, user_id={gg.user_id}")

    events_of_user = statistics.get_user_events(guest_user.id)
    print(f"Мероприятий у user {guest_user.id}: {len(events_of_user)}")
    for e in events_of_user:
        print(f"  • event_id={e.id}, date={e.date}")

    # -------- 6. Защита от повторной записи --------
    sub("2.6 Попытка записаться повторно (должно упасть)")
    try:
        users_option.add_guest(
            user_id=guest_user.id,
            event_id=existing_event_id,
            comments="Дубль",
        )
        print("!!! ОШИБКА: повторная запись прошла — UNIQUE не сработал")
    except Exception as ex:
        print(f"OK: {type(ex).__name__}")

    # -------- 7. Обновление записи --------
    sub("2.7 Обновление комментария гостя")
    updated = users_option.update_guest(g.id, comments="Уже не с друзьями, приду один")
    print(f"comments = {updated.comments!r}")

    # -------- 8. Отмена записи --------
    sub("2.8 Отмена записи (delete)")
    users_option.delete_guest(g.id)
    after = users_option.get_guests_by_event(existing_event_id)
    print(f"Гостей на меро после удаления: {len(after)}")

    return guest_user


# ============================================================
#  ТОЧКА ВХОДА
# ============================================================

if __name__ == "__main__":
    print("\n>>> ТЕСТОВЫЕ СЦЕНАРИИ ЛР №1 <<<")

    # Пересоздать схему — удобно для повторных запусков.
    # Если хочешь сохранить данные — закомментируй reset_db().
    reset_db()

    # Сценарий 1
    ev, org_user = scenario_organizer()

    # Сценарий 2 — использует мероприятие из первого сценария
    scenario_guest(existing_event_id=ev.id)

    section("ГОТОВО")
    print("Все сценарии выполнены без ошибок.\n")