from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
import os


## SQL URL
SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://"
    + os.environ["DB_USER"]
    + ":"
    + "%s"
    + "@"
    + os.environ["DB_URL"]
    + ":"
    + os.environ["DB_PORT"]
    + "/"
    + os.environ["DB_NAME"]
)


engine = create_engine(SQLALCHEMY_DATABASE_URL % quote_plus(os.environ["DB_PASSWORD"]))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        logging.info(" [SQL] : Connect to DB Ok")
        return db
    except:
        logging.info(" [SQL] : Connect to DB Failed")
