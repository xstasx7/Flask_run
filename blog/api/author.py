# Создаём все ресурсы для автора
from flask_combo_jsonapi import ResourceDetail, ResourceList
from combojsonapi.event.resource import EventsResource

from blog.shemas import AuthorSchema
from blog.models.database import db
from blog.models import Author, Article


class AuthorList(ResourceList):
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }


# Создаём AuthorDetailEvents: event_get_articles_count
class AuthorDetailEvents(EventsResource):
    def event_get_articles_count(self, **kwargs):
        return {"count": Article.query.filter(Article.author_id == kwargs["id"]).count()}


class AuthorDetail(ResourceDetail):
    events = AuthorDetailEvents
    schema = AuthorSchema
    data_layer = {
        "session": db.session,
        "model": Author,
    }
