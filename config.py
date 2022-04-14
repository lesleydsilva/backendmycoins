import os


SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
HOST = 'localhost'
PORT = '5432'

