from config.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    expenses = relationship("Expense", back_populates="user")

