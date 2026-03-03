from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
  table_id: int
  name: str
  image_url: str | None

class UserOut(UserCreate):
  id: int
  table_id: int
  created_at: datetime

  class Config:
    orm_mode = True
