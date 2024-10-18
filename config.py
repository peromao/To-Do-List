class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/todo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
