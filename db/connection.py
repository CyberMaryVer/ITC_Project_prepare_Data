from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

engine = create_engine(config.DATABASE_URL, echo=config.ECHO)
Session = sessionmaker(bind=engine)
session = Session()
