# Создаём блупринт юзеров
from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.models import User

# Создаем Blueprint
users_app = Blueprint("users_app", __name__)  # В Blueprint передаем название «приложения» и имя текущего файла

# USERS = {
#     1: "James",
#     2: "Brian",
#     3: "Peter",
# }  # Создаём словарь, который будет представлять БД с пользователями.


# view для обработки обращения к списку пользователей
# Добавляем имена этих view: endpoint. Теперь мы можем ссылаться на этот view по данному имени endpoint
@users_app.route("/", endpoint="list")
def users_list():
    users = User.query.filter(User.username).all()
    return render_template("users/list.html", users=users)


# Добавляем отрисовку шаблона с передачей выбранного пользователя
# Добавляем имена этих view: endpoint. Теперь мы можем ссылаться на этот view по данному имени endpoint
@users_app.route("/<int:user_id>/", endpoint="details")
def user_details(user_id: int):
    user = User.query.filter_by(id=user_id).one_or_none()
    if user is None:
        raise NotFound(f"User #{user_id} doesn't exist!")
    return render_template("users/details.html", user=user)

# @users_app.route("/<int:user_id>/", endpoint="details")
# def user_details(user_id: int):
#     try:  # Обработка ошибки, если пользователь не найден
#         user_name = USERS[user_id]
#     except KeyError:
#         raise NotFound(f"User #{user_id} doesn't exist!")
#     return render_template('users/details.html', user_id=user_id, user_name=user_name)
