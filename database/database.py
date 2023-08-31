# database.py
from distutils.util import execute

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
engine = create_engine('postgresql://lib:lib@postgres:5432/lib')
# engine = create_engine('postgresql://lib:lib@http://172.23.0.3:5432/lib')
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

