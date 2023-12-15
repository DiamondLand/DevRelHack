from fastapi import APIRouter, Request, UploadFile, File, Depends
from apps.activity import schemas, exceptions
import os, uuid, datetime
from user import depends, models
from apps.activity.models import Event, FeedBack
v1 = APIRouter()

@v1.post('/event')
async def create_event(r: Request, title: str, description: str, start_data: datetime.datetime, end_date:datetime.datetime, user: models.User = Depends(depends.get_user), file: UploadFile = File(...)):
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
    return await user.get_events()

@v1.post('/event/feedback')
async def create_feedback(r: Request, data: schemas.CreateFeedback, user: models.User = Depends(depends.get_user)):
    event = await Event.get(id=data.event_id)
    if event in await user.events.all():
        raise exceptions.ErrorFeedBackForMe
    feed = FeedBack(
        comment=data.comment,
        stars=data.starts,
        from_user=user,
    )
    
    await feed.save()
    await event.feedbacks.add(feed)
    return {
        "status": True
    }

@v1.get('/event/feedback')
async def get_feedbacks(r: Request, event_name: str, user: models.User = Depends(depends.get_user)):
    event = await Event.get(title=event_name)
    return await event.get_feedbacks()

