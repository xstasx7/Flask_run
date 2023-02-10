# Создаём модель Автора в, добавляем связь с пользователем
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from blog.models.database import db


class Author(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="author")  # связь с пользователем «один к одному»
    articles = relationship("Article", back_populates="author")  # Обратная связь со статьями «один ко многим»

    # def __str__(self):  # Строковые данные для моделей чтобы в админке модели отображались в понятном виде
    #     return self.user_id

