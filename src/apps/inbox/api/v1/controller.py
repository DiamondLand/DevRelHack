from fastapi import APIRouter
from fastapi import APIRouter, Request, UploadFile, File, Depends
from apps.inbox import models, exceptions
from user import depends
from user import models as userModels
import os, uuid

v1 = APIRouter()

@v1.post('/message')
async def create_message(r: Request,  title: str, content: str,
                         file1: UploadFile  = File(None),
                         file2: UploadFile | None = File(None),
                         file3: UploadFile | None = File(None),
                         to_user: userModels.User = Depends(depends.get_user_by_username),
                         user: userModels.User = Depends(depends.get_user)):
    
    
    save_files = []
    save_files_orm = []
    for f in [file1, file2, file3]:
        if f != None:
            save = os.path.join(os.getcwd(), 'public', 'static', 'images', str(uuid.uuid4()) + '.' + f.filename.split('.')[-1])
            with open(save, 'wb') as user_file:
                user_file.write(f.file.read())
            save_files.append(save)
            
    for path in save_files:
        save_files_orm.append(await models.File.create(file_path=path))
        
    msg = models.Message(
        title=title,
        content=content,
        to_user=to_user,
        from_user=user
    )
    
    await msg.save()
    for f in save_files_orm:
        await msg.files.add(f)
        
    return {
        'status': True
    }
    
@v1.get('/message')
async def get_messages(user: userModels.User = Depends(depends.get_user)):
    messages = await models.Message.filter(to_user=user)
    data = []
    for msg in messages:
        data.append(await msg.json())
    return data

@v1.get('/message/immediate')
async def get_message(id: int, user: userModels.User = Depends(depends.get_user)):
    messages = await models.Message.filter(from_user=user)
    data = []
    for msg in messages:
        data.append(await msg.json())
    return data

@v1.post("/mark_as_viewed/{message_id}")
async def mark_as_viewed(message_id: int, to_user: userModels.User = Depends(depends.get_user)):
    message = await models.Message.filter(id=message_id, to_user=to_user).first()

    if not message:
        raise exceptions.ErrorMessageNotFound

    message.viewed = True
    await message.save()

    return {
        'status': True
    }