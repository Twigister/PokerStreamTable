from sqlalchemy import Column, Integer, String, DateTime, func
from app.db import Base

# Link for multiple tables, might be useful to support MTTs
# class House(Base):
#   pass

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), nullable=False)
  image_url = Column(String, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  status = Column(String(20), nullable=False) # Utiliser un enum? 
  table_id = Column(Integer, nullable=True) # TODO store as a db link
  seat_number = Column(Integer, nullable=True)

class Player(Base):
  __tablename__ = "players"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(100), nullable=False)
  image_url = Column(String, nullable=True)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  status = Column(String(20), nullable=False)
  table_id = Column(Integer, nullable=True)
  seat_number = Column(Integer, nullable=True)

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

class Wallet(Base):
  __tablename__ = "wallets"

  id = Column(Integer, primary_key=True, index=True)
  owner_id = Column(Integer, nullable=False)
  currency = Column(String(10), nullable=False)
  
class Ledger(Base):
  __tablename__ = "ledgers"

  id = Column(Integer, primary_key=True, index=True)
  wallet_id = Column(Integer, nullable=False)
  amount = Column(Integer, nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
