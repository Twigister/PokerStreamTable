# Create Read Update Delete

from sqlalchemy.orm import Session
from app import models, schemas

def get_users(db: Session, skip=0, limit=10):
  res = db.query(models.User).offset(skip).limit(limit).all()
  return res

def create_user(db: Session, user_data: schemas.UserCreate):
  new_user = models.User(
    name=user_data.name,
    image_url=user_data.image_url,
    status="offline",
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if user:
    user.name = user_data.name
    user.image_url = user_data.image_url
    db.commit()
    db.refresh(user)
  return user

def delete_user(db: Session, user_id: int):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if user:
    db.delete(user)
    db.commit()
  return user

def get_table_state(db: Session, table_id: int):
  res = db.query(models.User).filter(models.User.table_id == table_id).filter(models.User.seat_number != None).all()
  return res

def seat_user(db: Session, user_id: int, table_id: int, seat_number: int):
  res = db.query(models.User).filter(models.User.id == user_id).first()
  if res:
    res.table_id = table_id
    res.seat_number = seat_number
    db.commit()
    db.refresh(res)
  return res

def unseat_user(db: Session, user_id: int):
  res = db.query(models.User).filter(models.User.id == user_id).first()
  if res:
    res.table_id = None
    res.seat_number = None
    db.commit()
    db.refresh(res)
  return res