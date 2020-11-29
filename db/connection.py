from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

engine = create_engine(config.DATABASE_URL + '/' + config.DATABASE_NAME, echo=config.ECHO)
Session = sessionmaker(bind=engine)
session = Session()
