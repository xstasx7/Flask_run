# Переносим конфигурации в классы
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"  # URI для подключения к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Не Отслеживать изменения объектов и отправлять сигналы
    SECRET_KEY = "abcdefg123456"  # Для работы авторизации обязательно нужен SECRET_KEY в конфигурации
    WTF_CSRF_ENABLED = True  # Включаем защиту CSRF
    FLASK_ADMIN_SWATCH = 'cosmo'  # Тема для админки
    OPENAPI_URL_PREFIX = '/api/swagger'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_VERSION = '3.22.0'


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True


