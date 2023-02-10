from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from blog.models.database import db
from blog.models import User, Tag
from blog.forms.user import RegistrationForm, LoginForm

# Создаем Blueprint
auth_app = Blueprint("auth_app", __name__)

login_manager = LoginManager()  # Инициализируем объект для обработки авторизации
login_manager.login_view = "auth_app.login"  # Указываем view для авторизации


@login_manager.user_loader  # Вытаскиваем искомого пользователя (по ID);
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler  # Указываем обработку не авторизированной попытки доступа к защищённым view.
def unauthorized():
    return redirect(url_for("auth_app.login"))  # Выполняем редирект на страницу авторизации


# view для регистрации
# view для входа просто по юзернейму
@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:
        return redirect("index")

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        # temp = form.username.data
        # db.create_all()
        user = User.query.filter_by(username=form.username.data).one_or_none()
        if user is None:
            return render_template("auth/login.html", form=form, error="username doesn't exist")
        if not user.validate_password(form.password.data):
            return render_template("auth/login.html", form=form, error="invalid username or password")

        login_user(user)
        return redirect(url_for("index"))

    return render_template("auth/login.html", form=form)
    # if request.method == "GET":
    #     return render_template("auth/login.html")
    #
    # username = request.form.get("username")
    # if not username:
    #     return render_template("auth/login.html", error="username not passed")
    #
    # user = User.query.filter_by(username=username).one_or_none()
    # if user is None:
    #     return render_template("auth/login.html", error=f"no user {username!r} found")
    #
    # login_user(user)
    # return redirect(url_for("index"))


# Авторизацию по юзернейму оставляем админу в виде login-as
@auth_app.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):
        # Пользователи без прав администратора не должны знать об этой функции
        raise NotFound


# view для вЫхода
@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# view, которое требует авторизации чтобы его можно было посмотреть
@auth_app.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"


# Добавляем регистрацию. Используем форму для проверки введенных данных, валидируем почту и юзернейм.
@auth_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect("index")

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/register.html", form=form, error=error)


#  Указываем объекты, которые будем импортировать
__all__ = [
    "login_manager",
    "auth_app",
]
