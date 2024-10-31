from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.beckend.db_depends import get_db
from typing import Annotated
from app.models.task import Task
from app.models.user import User

from sqlalchemy import insert, select, update, delete
from app.schemas import CreateTask, UpdateTask

from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tas = db.scalars(select(Task)).all()
    return tas

@router.get("/task_id")
def task_by_id( db: Annotated[Session, Depends(get_db)],task_id: int):
    # Получение пользователя по id
    tas = db.scalar(select(Task).where(Task.id == task_id))
    if tas is not None:
        return tas
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')

@router.post('/create')
def create_task(db: Annotated[Session, Depends(get_db)], create_tasks: CreateTask, user_id: int):
    # Проверка на существование пользователя
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

    db.execute(insert(Task).values(title=create_tasks.title,
                                   content=create_tasks.content,
                                   priority=create_tasks.priority,
                                   user_id=existing_user.id,
                                   slug=slugify(create_tasks.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_tasks: UpdateTask):
    tas = db.scalar(select(Task).where(Task.id == task_id))
    if tas is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    db.execute(update(Task).where(Task.id == task_id).values(
        title=update_tasks.title,
        content=update_tasks.content,
        priority=update_tasks.priority,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'
    }

@router.delete("/delete")
def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tas = db.scalar(select(Task).where(Task.id == task_id))
    if tas is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'
    }