import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASS = os.environ.get("MYSQL_PASS")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")

class DevConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


class ProdConfig(DevConfig):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'