from pathlib import Path
import secrets
basedir = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = secrets.token_urlsafe(32)
    WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    "testing": TestingConfig,
    "local": LocalConfig,
    "production": ProductionConfig,
}
