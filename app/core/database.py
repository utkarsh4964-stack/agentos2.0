import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway provides DATABASE_URL for Postgres. Falls back to local SQLite for
# quick local testing without needing Postgres installed.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentos.db")

# Railway's Postgres URL sometimes starts with "postgres://" but SQLAlchemy
# needs "postgresql://" - fix it automatically.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
