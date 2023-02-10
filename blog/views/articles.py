from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import joinedload

from blog.models.database import db
from blog.models import Author, Article
from blog.forms.article import CreateArticleForm
from blog.models.tag import Tag

# Создаем Blueprint
articles_app = Blueprint("articles_app", __name__)  # В Blueprint передаем название «приложения» и имя текущего файла


# ARTICLES = ["Flask", "Django", "JSON:API"]

@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


# Добавляем имена этих view: endpoint. Теперь мы можем ссылаться на этот view по данному имени endpoint
# @articles_app.route("/", endpoint="list")
# def articles_list():
#     return render_template("articles/list.html", articles=ARTICLES)

@articles_app.route("/<int:article_id>/", endpoint="details")
def article_detals(article_id):
    article = Article.query.filter_by(id=article_id).options(
        joinedload(Article.tags)).one_or_none()  # подгружаем связанные теги с объединенной нетерпеливой загрузки
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


# Добавляем view для создания статей и авторизацию пользователя.
# При создании статьи к модели пользователя добавляется модель автора, если её ещё нет.
# Модель статьи привязывается к модели автора
@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]  # добавляем доступные теги в форму
    if request.method == "POST" and form.validate_on_submit():  # при создании статьи
        article = Article(title=form.title.data.strip(), body=form.body.data)
        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)  # добавляем выбранные теги к статье
        db.session.add(article)
        if current_user.author:
            # использовать существующего автора, если он есть
            article.author = current_user.author
        else:
            # в противном случае создайте запись об авторе
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author = current_user.author

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Не удалось создать новую статью!")
            error = "Не удалось создать статью!"
        else:
            return redirect(url_for("articles_app.details", article_id=article.id))

    return render_template("articles/create.html", form=form, error=error)