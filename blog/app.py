from time import time
from flask import Flask, render_template
from flask import request
from flask import g
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.security import flask_bcrypt
from blog.views.authors import authors_app
from blog.admin import admin
from blog.api import init_api

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # Cоздаём Flask app, в него передаём имя текущего файла

cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
app.config.from_object(f"blog.configs.{cfg_name}")  # Переопределяем нужные параметры из configs.py

admin.init_app(app)  # Инициализируем приложение Flask-Admin

api = init_api(app)  # Инициализируем приложение API

flask_bcrypt.init_app(app)  # Инициализируем приложение Flask-Bcrypt

migrate = Migrate(app, db, compare_type=True)  # Инициализируем приложение Flask-Migrate

# Подключаем LoginManager
login_manager.init_app(app)  # Flask-Login работает через менеджер входа в системы

# Подключаем блупринты и указываем приложению, какой url_prefix использовать для всех вложенных views
app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(authors_app, url_prefix="/authors")
app.register_blueprint(articles_app, url_prefix="/articles")

db.init_app(app)  # Код для работы с БД


# Создаем index view: обрабатываем обращение на корень сайта, отдаём обычный текст
@app.route("/",
           methods=["GET", "POST"])  # Указываем, что данный view должен быть использован для обработки запроса на /
def index():
    return render_template("index.html")


# Для инициализации базы при первом запуске
# @app.cli.command("init-db")
# def init_db():
#     """
#     Запустите в своем терминале:
#     flask init-db
#     """
#     db.create_all()
#     print("done!")


#  Создает пользователей (admin)
@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)


# Создаём новую команду для Тегов (flask create-tags)
@app.cli.command("create-tags")
def create_tags():
    """Запустите в своем терминале:
    ➜ flask create-tags
    """
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()
    print("created tags")

#  Создавать пользователей
# @app.cli.command("create-users")
# def create_users():
#     """
#     Запустите в своем терминале:
#     flask create-users
#     > done! созданные пользователи: <User #1 'admin'> <User #2 'james'>
#     """
#     from blog.models import User
#     admin = User(username="admin", is_staff=True)
#     james = User(username="james")
#
#     db.session.add(admin)
#     db.session.add(james)
#     db.session.commit()
#     print("done! созданные пользователи:", admin, james)

#######################################################################################################


# # Variable Rules, переменные части в URL-адрес,
# @app.route("/greet/<name>/")
# def greet_name(name: str):  # Используем конвертер, чтобы указать тип аргумента
#     return f"Hello {name}!"
#
#
# # Обрабатываем параметры запроса (query string)
# @app.route("/user/")
# def read_user():
#     name = request.args.get("name")  # Для обращения к query string необходимо использовать request.args
#     surname = request.args.get("surname")  # Используем .get, потому что с request.args нужно обращаться как со словарём
#     return f"User {name or '[no name]'} {surname or '[no surname]'}"
#
#
# # Обрабатываем тело запроса и возвращаем кастомные статус-коды
# @app.route("/status/", methods=["GET", "POST"])  # Указать допустимые методы через именованную переменную method
# def custom_status_code():
#     if request.method == "GET":  # Через request.method проверяем, что метод GET.
#         return """\
#         Чтобы получить ответ с пользовательским кодом состояния
#         нужно отправить запрос методом POST
#         и передать `код` в тело JSON / FormData
#         """  # Возвращаем инструкцию, как пользоваться данным endpoint
#
#     print("raw bytes data:", request.data)
#     #  Если POST, то выполняем обработку данных.
#     if request.form and "code" in request.form:  # Проверяем request.form, работаем с объектом как со словарём
#         return "code from form", request.form["code"]  # отдаём ответ с таким кодом
#
#     if request.json and "code" in request.json:  # Проверяем request.json, работаем с объектом как со словарём
#         return "code from json", request.json["code"]  # отдаём ответ с таким кодом
#
#     return "", 204  # По умолчанию отдаём пустой ответ с кодом 204.
#
#
# # Обработчики before_request, after_request; объект g
# @app.before_request  # Добавляем обработчики, вызываемые до запроса и после
# def process_before_request():
#     """
#     Устанавливает start_time в объект `g`
#     """
#     g.start_time = time()
#
#
# @app.after_request
# def process_after_request(response):
#     """
#     добавляет время обработки в заголовки
#     """
#     if hasattr(g, "start_time"):
#         response.headers["process-time"] = time() - g.start_time
#     return response
#
#
# @app.route("/power/")
# def power_value():
#     x = request.args.get("x") or ""
#     y = request.args.get("y") or ""
#     if not (x.isdigit() and y.isdigit()):
#         app.logger.info("неверные значения мощности: x=%r and y=%r", x, y)
#         raise BadRequest(
#             "пожалуйста, передайте целые числа `x` и `y` в параметрах запроса")  # http://127.0.0.1:5000/power/
#
#     x = int(x)
#     y = int(y)
#     result = x ** y  # http://127.0.0.1:5000/power/?x=7&y=3
#     app.logger.debug("%s ** %s = %s", x, y, result)
#     return str(result)
#
#
# #  Обработка непредвиденных исключений
# @app.route("/divide-by-zero/")
# def do_zero_division():  # Будет вызывать исключение
#     return 1 / 0
#
#
# @app.errorhandler(ZeroDivisionError)  # Передаём туда исключение, которое собираемся ловить
# def handle_zero_division_error(error):  # Регистрируем обработчик handle_zero_division_error
#     print(error)  # Печатает str версию ошибки: "деление на ноль"
#     app.logger.exception("Вот трассировка для ошибки деления на ноль")
#     return "Никогда не делить на ноль!", 400
