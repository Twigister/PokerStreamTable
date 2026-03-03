from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base

# Link for multiple tables, might be useful to support MTTs
# class House(Base):
#   pass

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  table_id = Column(Integer, nullable=False) # TODO store as a link
  name = Column(String(100), nullable=False)
  image_url = Column(String, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())

class Table(Base):
  __tablename__ = "tables"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  # The options for table config will be stored here
  # IG: timer_color/led_offset/Etc

# class Session(Base):
#   __tablename__ = "sessions"

#   id = Column(Integer, primary_key=True, index=True) # La session doit être appairée à la table
#   game_type = Column(String(10), nullable=False)

# Contains history of a played hand. Future
# class Hand(Base):
#   __tablename__ = "hands"
