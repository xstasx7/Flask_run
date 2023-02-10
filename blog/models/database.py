# Инициализируем объект SQLAlchemy для работы с БД
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = [
    "db",
]
