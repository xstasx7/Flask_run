from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from blog.models.database import db
from flask_login import UserMixin  # UserMixin обеспечивает реализацию свойств Flask-Login в модели пользователя
from blog.security import flask_bcrypt
from sqlalchemy.orm import relationship


# Создаём декларативную модель, наследуемся от предоставляемой базы db.Model;
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), nullable=False, default="", server_default="")
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    is_staff = Column(Boolean, nullable=False, default=False)
    _password = Column(LargeBinary, nullable=True)

    author = relationship("Author", uselist=False, back_populates="user")  # обратную связь с пол-ем «один к одному»

    # Добавляем пароль пользователю
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)

    def __repr__(self):  # Добавляем функцию для отображения репрезентативного вида.
        return f"<User #{self.id} {self.username!r} {self.email} {self.first_name} {self.last_name}>"
