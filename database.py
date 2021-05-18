import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://ewcvjdinvklqyr:5aee9fa1d8e68601148715ebbeacd8f6344ba8407bb808c47ffddb52b394b09a@ec2-54-73-58-75.eu-west-1.compute.amazonaws.com:5432/d5jd0nu9752dpa'  # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
