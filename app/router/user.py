from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.beckend.db_depends import get_db
from typing import Annotated
from app.models.user import User
from app.models.task import Task
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser

from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/create')
def create_user(db: Annotated[Session, Depends(get_db)], create_users: CreateUser):
    # Проверка на существование пользователя
    existing_user = db.scalar(select(User).where(User.username == create_user.username))
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

    db.execute(insert(User).values(username=create_users.username,
                                   firstname=create_users.firstname,
                                   lastname=create_users.lastname,
                                   age=create_users.age,
                                   slug=slugify(create_users.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# ---------------------------------
# ---------------------------------


@router.get('/user_id')
def user_by_id( db: Annotated[Session, Depends(get_db)],user_id: int):
    # Получение пользователя по id
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    

@router.get('/')
def all_users(db: Annotated[Session, Depends(get_db)]):
    username = db.scalars(select(User)).all()
    return username


# -----------------------------
@router.put('/update_user')
def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_users: UpdateUser):
    usernames = db.scalar(select(User).where(User.id == user_id))
    if usernames is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(
        firstname=update_users.firstname,
        lastname=update_users.lastname,
        age=update_users.age,
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


# -----------------------------------------------


# @router.delete('/delete')
# def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
#     user = db.scalar(select(User).where(User.id == user_id))
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
#     db.execute(delete(User).where(User.id == user_id))
#     db.commit()
#     return {
#         'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'
#     }


# # Удаление всех пользователей и задач из базы данных для теста
# @router.delete("/deleteAll")
# def delete_all_users(db: Annotated[Session, Depends(get_db)]):
#     # Проверяем, есть ли пользователи в базе данных
#     result = db.execute(select(User)).scalars().all()
#
#     if result:  # Если список пользователей не пуст
#         db.execute(delete(User))
#         db.commit()
#         return {'status_code': status.HTTP_200_OK, 'transaction': 'All users and tasks deleted!'}
#     else:  # Если список пользователей пуст
#         return {'status_code': status.HTTP_200_OK, 'transaction': 'No users and tasks to delete'}

@router.get("/user_id/tasks")
def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(User.id == user_id)).all()
    return tasks

@router.delete('/delete')
def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK, 'transaction': 'User and tasks delete is successful!'
    }