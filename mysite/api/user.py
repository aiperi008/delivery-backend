from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import User
from mysite.database.schemas import UserOutSchema, UserInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/user', tags=['User'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post('/', response_model=UserOutSchema)
async def create_user(user: UserInputSchema, db: Session = Depends(get_db)):
    user_db = User(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/', response_model=List[UserOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get('/{user_id}/', response_model=UserOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Пользователь не найден', status_code=400)

    return user_db


@user_router.put('/{user_id}/', response_model=dict)
async def update_user(user_id: int, user: UserInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Пользователь не найден', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Пользователь изменен'}


@user_router.delete('/{user_id}/', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Пользователь не найден', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'message': 'Пользователь удален'}