from sqlalchemy import create_engine
from db.entities import Base
import config


def main():
    """ Create the database """
    engine = create_engine(config.DATABASE_URL, echo=config.ECHO)
    engine.execute(f'CREATE DATABASE IF NOT EXISTS {config.DATABASE_NAME}')
    engine.execute('USE stack_exchange')

    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error while creating {config.DATABASE_NAME} database!')
        print(e)
    else:
        print(f'{config.DATABASE_NAME} database created successfully!')
