# Create Read Update Delete

from sqlalchemy.orm import Session
from app import models, schemas

def get_users(db: Session, skip=0, limit=10):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user_data: schemas.UserCreate):
  new_user = models.User(
    table_id=user_data.table_id,
    name=user_data.name,
    image_url=user_data.image_url
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user