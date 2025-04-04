import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL


logging.basicConfig(
    format="SQL --->  %(message)s",
    level=logging.INFO
)

@event.listens_for(Engine, "before_cursor_execute")
def log_sql_query(conn, cursor, statement, parameters, context, executemany):
    logging.info(f"{statement}")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
