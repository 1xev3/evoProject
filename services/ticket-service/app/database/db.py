from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import path, getenv, getcwd

if not load_dotenv(dotenv_path = 'app/.env'):
    print("\n[db.py] DOTENV NOT LOADED!\n"*3)
    exit(404)

SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()