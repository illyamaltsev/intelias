import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "SecretKey01")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///../test.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
