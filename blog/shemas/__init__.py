# Добавляем все схемы
from blog.shemas.tag import TagSchema
from blog.shemas.user import UserSchema
from blog.shemas.author import AuthorSchema
from blog.shemas.article import ArticleSchema


__all__ = [
    "TagSchema",
    "UserSchema",
    "AuthorSchema",
    "ArticleSchema",
]
