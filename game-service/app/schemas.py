from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
  name: str
  image_url: str | None

class UserUpdate(BaseModel):
  name: str
  image_url: str | None

class UserOut(UserCreate):
  id: int
  table_id: int | None
  created_at: datetime
  seat_number: int | None

  model_config = {
    "from_attributes": True
  }

  # class Config:
  #   orm_mode = True

class SeatUser(BaseModel):
  user_id: int
  table_id: int
  seat_number: int

class UnseatUser(BaseModel):
  user_id: int