from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from db.entities import Base

engine = create_engine('mysql+pymysql://root:root@localhost:3306/stack_exchange', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
