from .base import SessionLocal


def get_db():
    return SessionLocal()
