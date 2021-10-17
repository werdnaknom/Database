import os

# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # LOGGING CONFIG
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")

    # BABEL Config
    LANGUAGES = {
        "en": "English",
    }
    MONGO_URI = os.environ.get("MONGO_URI")

    basedir = os.path.abspath(os.path.dirname(__file__))

class DeploymentConfig(Config):
    OR_DIRECTORY_HEAD = os.environ.get("OR_ATS_DIRECTORY") or r'F:\ATS DATABASE'
    KM_DIRECTORY_HEAD = os.environ.get("KM_ATS_DIRECTORY") or r'F:\ATS DATABASE'


class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True

    # MONGODB SETUP
    MONGO_URI = "mongodb://localhost:27017"  # Must setup in standalone docker
    redis_port = 6379
    REDIS_URL = 'redis://localhost'
    OR_DIRECTORY_HEAD = r'F:\ATS DATABASE'
    KM_DIRECTORY_HEAD = r'F:\ATS DATABASE'
