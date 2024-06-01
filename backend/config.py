import os

class Config():
    DEBUG=False
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI=None

class LocalDev(Config) :
    SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite3'
    DEBUG=True
    SECRET_KEY='gnjdgd45g1hmjn545'
    SECURITY_PASSWORD_SALT="really_secret"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECURITY_REGISTERABLE=True
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW=None
    WTF_CSRF_ENABLED=False
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_TOKEN_AUTHENTICATION_HEADER='Authentication-Token'
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3
