import os
import uuid
import datetime

from fastapi import APIRouter, Request, UploadFile, File, Depends, HTTPException
from apps.activity.models import Event, FeedBack
from apps.activity import schemas, exceptions
from user import depends, models

v1 = APIRouter()


@v1.post('/event')
async def create_event(r: Request, title: str, description: str,
                       start_data: datetime.datetime, end_date: datetime.datetime,
                       user: models.User = Depends(depends.get_user),
                       file: UploadFile = File(...)):
    """
    Создает новое событие.

    Параметры:
    - title (str): Название события.
    - description (str): Описание события.
    - start_date (datetime.datetime): Дата и время начала события.
    - end_date (datetime.datetime): Дата и время окончания события.
    - user (models.User): Пользователь, создающий событие.
    - file (UploadFile): Изображение для события.

    Возвращает:
    - dict: Словарь с состоянием операции.
    """

    save = os.path.join(os.getcwd(), 'public', 'static', 'images', str(uuid.uuid4()) + '.png')
    with open(save, 'wb') as f:
        f.write(file.file.read())

    event = Event(
        title=title,
        description=description,
        strat_date=start_data,
        end_date=end_date,
        photo_path=save,
    )
    await event.save()
    await user.events.add(event)

    return {
        "status": True
    }


@v1.get('/event')
async def get_events(r: Request, user: models.User = Depends(depends.get_user)):
    """
    Получает события, связанные с аутентифицированным пользователем.

    Параметры:
    - user (models.User): Аутентифицированный пользователь.

    Возвращает:
    - List[Event]: Список событий, связанных с пользователем.
    """

    return await user.get_events()


@v1.post('/event/feedback')
async def create_feedback(r: Request, data: schemas.CreateFeedback, user: models.User = Depends(depends.get_user)):
    """
    Создает обратную связь для определенного события.

    Параметры:
    - data (schemas.CreateFeedback): Данные обратной связи, включая event_id, комментарий и звезды.
    - user (models.User): Пользователь, создающий обратную связь.

    Возвращает:
    - dict: Словарь с состоянием операции.
    """

    event = await Event.get(id=data.event_id)
    for feed in await event.feedbacks.all():
        if await feed.from_user.get() == user:
            raise exceptions.ErrorAlreadyFeedback

    if event in await user.events.all():
        raise exceptions.ErrorFeedBackForMe

    feed = FeedBack(
        comment=data.comment,
        stars=data.stars,
        from_user=user,
    )

    await feed.save()
    await event.feedbacks.add(feed)
    return {
        "status": True
    }



@v1.get('/event/feedback')
async def get_feedbacks(r: Request, event_id: int, user: models.User = Depends(depends.get_user)):
    """
    Получает обратную связь для определенного события.

    Параметры:
    - event_name (str): Название события.
    - user (models.User): Аутентифицированный пользователь.

    Возвращает:
    - List[FeedBack]: Список обратной связи, связанный с событием.
    """

    event = await Event.get(id=event_id)
    return await event.get_feedbacks()


@v1.post('/event/update/title')
async def update_event_title(r: Request, event_id: int, title: str, user: models.User = Depends(depends.get_user)):
    """
    Обновление названия события.

    Параметры:
    - event_id (int): Уникальный идентификатор события.
    - title (str): Новое название события.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если событие с заданным event_id не найдено или если у пользователя нет доступа.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
    """

    event = await Event.get(id=event_id)
    if event in await user.events.all():
        event.title = title
        await event.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/update/description')
async def update_description_title(r: Request, event_id: int, description: str, user: models.User = Depends(depends.get_user)):
    """
    Обновление описания события.

    Параметры:
    - event_id (int): Уникальный идентификатор события.
    - description (str): Новое описание события.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если событие с заданным event_id не найдено или если у пользователя нет доступа.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
          Пример: {"status": True}
    """

    event = await Event.get(id=event_id)
    if event in await user.events.all():
        event.description = description
        await event.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/update/strat_date')
async def update_strat_date_title(r: Request, event_id: int, strat_date: datetime.datetime, user: models.User = Depends(depends.get_user)):
    """
    Обновление начальной даты события.

    Параметры:
    - event_id (int): Уникальный идентификатор события.
    - strat_date (datetime.datetime): Новая начальная дата события.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если событие с заданным event_id не найдено или если у пользователя нет доступа.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
    """

    event = await Event.get(id=event_id)
    if event in await user.events.all():
        event.strat_date = strat_date
        await event.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/update/end_date')
async def update_end_date_title(r: Request, event_id: int, end_date: datetime.datetime, user: models.User = Depends(depends.get_user)):
    """
    Обновление конечной даты события.

    Параметры:
    - event_id (int): Уникальный идентификатор события.
    - end_date (datetime.datetime): Новая конечная дата события.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если событие с заданным event_id не найдено или если у пользователя нет доступа.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
    """
     
    event = await Event.get(id=event_id)
    if event in await user.events.all():
        event.end_date = end_date
        await event.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/delete')
async def delete_event(r: Request, event_id: int, user: models.User = Depends(depends.get_user)):
    """
    Удаление события.

    Параметры:
    - event_id (int): Уникальный идентификатор события.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если событие с заданным event_id не найдено или если у пользователя нет доступа.

    Возвращает:
    dict: Словарь, содержащий статус операции удаления.
    """
    event = await Event.get(id=event_id)
    if event in await user.events.all():
        await event.delete()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/feedback/update/comment')
async def update_feedback_comment(r: Request, feedback_id: int, comment: str, user: models.User = Depends(depends.get_user)):
    """
    Обновление комментария к обратной связи.

    Параметры:
    - feedback_id (int): Уникальный идентификатор обратной связи.
    - comment (str): Новый комментарий к обратной связи.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если обратная связь с заданным feedback_id не найдена или если пользователь не является автором этой обратной связи.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
    """

    feed = await FeedBack.get(id=feedback_id)
    if await feed.from_user.get() == user:
        feed.comment = comment
        await feed.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/feedback/update/stars')
async def update_feedback_stars(r: Request, feedback_id: int, stars: int, user: models.User = Depends(depends.get_user)):
    """
    Обновление количества звезд в обратной связи.

    Параметры:
    - feedback_id (int): Уникальный идентификатор обратной связи.
    - stars (int): Новое количество звезд в обратной связи.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если обратная связь с заданным feedback_id не найдена или если пользователь не является автором этой обратной связи.

    Возвращает:
    dict: Словарь, содержащий статус операции обновления.
    """

    feed = await FeedBack.get(id=feedback_id)
    if await feed.from_user.get() == user:
        feed.stars = stars
        await feed.save()
        return {
            "status": True
        }
    raise HTTPException(404)


@v1.post('/event/feedback/delete')
async def delete_feedback(r: Request, feedback_id: int, user: models.User = Depends(depends.get_user)):
    """
    Удаление обратной связи.

    Параметры:
    - feedback_id (int): Уникальный идентификатор обратной связи.
    - user (models.User, опционально): Пользователь, совершающий запрос. По умолчанию - аутентифицированный пользователь.

    Исключения:
    - HTTPException(404): Вызывается, если обратная связь с заданным feedback_id не найдена или если пользователь не является автором этой обратной связи.

    Возвращает:
    dict: Словарь, содержащий статус операции удаления.
    """

    feed = await FeedBack.get(id=feedback_id)
    if await feed.from_user.get() == user:
        await feed.delete()
        return {
            "status": True
        }
    raise HTTPException(404)