# Создаём первый API ресурс
from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.shemas import TagSchema
from blog.models.database import db
from blog.models import Tag


class TagList(ResourceList):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }
