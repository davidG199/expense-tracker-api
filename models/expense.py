from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from config.database import Base
from sqlalchemy.orm import relationship

class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String)
    category = Column(String)
    date = Column(DateTime)
    mount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="expenses")
