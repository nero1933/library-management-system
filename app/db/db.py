import logging

from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core import settings

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO)


@event.listens_for(Engine, "before_cursor_execute")
def log_sql_query(conn, cursor, statement, parameters, context, executemany):
    if not settings.DISABLE_SQL_LOGGING:
        logging.info(f"SQL --->  {statement}")


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
