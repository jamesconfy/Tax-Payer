import os
from dotenv import load_dotenv
load_dotenv()

class DevConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


class ProdConfig(DevConfig):
    SQLALCHEMY_DATABASE_URI = ''