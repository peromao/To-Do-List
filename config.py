import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/todo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://localhost:6379/0'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'ahQvKzRs')

    DEBUG = True
