# SQLAlchemy engine configuration ###########################################################################
# To see more info about how to configure the database url
# you can visit https://docs.sqlalchemy.org/en/13/core/engines.html
DATABASE_NAME = 'stack_exchange'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'root'
DATABASE_LOCATION = 'localhost:3306'

DATABASE_URL = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_LOCATION}/{DATABASE_NAME}'
ECHO = False
#############################################################################################################
