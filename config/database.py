from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.baseSettings import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
