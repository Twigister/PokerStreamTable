from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

# TODO check if table exists

@router.post("/", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
  return crud.create_user(db, user_in)

@router.get("/", response_model=list[schemas.UserOut])
def read_users(db: Session = Depends(get_db)):
  return crud.get_users(db)

@router.post("/seat", response_model=schemas.UserOut)
def seat_user(seat_data: schemas.SeatUser, db: Session = Depends(get_db)):
  return crud.seat_user(db, user_id=seat_data.user_id, table_id=seat_data.table_id, seat_number=seat_data.seat_number)

@router.post("/unseat", response_model=schemas.UserOut)
def unseat_user(unseat_data: schemas.UnseatUser, db: Session = Depends(get_db)):
  user = crud.unseat_user(db, user_id=unseat_data.user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return user

@router.get("/getTableState", response_model=list[schemas.UserOut | None])
def get_table_state(table_id: int = 1, db: Session = Depends(get_db)):
  users = crud.get_table_state(db, table_id) 
  res = [None] * 10
  for u in users:
    res[u.seat_number - 1] = u
  return res

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
  user = crud.update_user(db, user_id, user_in)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  existing_user = crud.get_user(db, user_id)
  if existing_user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  if existing_user.table_id is not None or existing_user.seat_number is not None:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unseat the player before deleting")

  user = crud.delete_user(db, user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
