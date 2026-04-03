from sqlalchemy import create_engine 
from sqlalchemy import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///media_finance.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine) # 001_app.py
Base = declarative_base()