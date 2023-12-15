from pydantic import BaseModel
import datetime

class CreateEvent(BaseModel):
    title: str
    description: str
    start_data: datetime.datetime
    end_date: datetime.datetime

class CreateFeedback(BaseModel):
    comment: str
    starts: int
    event_id: int
    
