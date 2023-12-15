
from fastapi import APIRouter, Request, Depends, UploadFile, File, UploadFile
from user import models, depends, utils
from apps.inbox import models as inbox_models
import os, uuid

v1 = APIRouter(prefix='/admin', tags=['admin'])

@v1.post('/newsletter')
async def create_newsletter(request: Request, title: str, content: str,
                         file1: UploadFile = File(None),
                         file2: UploadFile = File(None),
                         file3: UploadFile = File(None),
                         user: models.User = Depends(depends.admin_user)):
    save_files = []
    save_files_orm = []
    for f in [file1, file2, file3]:
        if f != None:
            save = os.path.join(os.getcwd(), 'public', 'static', 'images', str(
                uuid.uuid4()) + '.' + f.filename.split('.')[-1])
            with open(save, 'wb') as user_file:
                user_file.write(f.file.read())
            save_files.append(save)

    for path in save_files:
        save_files_orm.append(await inbox_models.File.create(file_path=path))
        
    for db_user in await models.User.all():
        msg = inbox_models.Message(
            title=title,
            content=content,
            to_user=db_user,
            from_user=user
        )

        await msg.save()
        for f in save_files_orm:
            await msg.files.add(f)
            
    return {
        'status': True
    }