from db.connection import engine
from db.entities import Base

engine.execute('CREATE DATABASE IF NOT EXISTS stack_exchange')
engine.execute('USE stack_exchange')

Base.metadata.create_all(bind=engine)
