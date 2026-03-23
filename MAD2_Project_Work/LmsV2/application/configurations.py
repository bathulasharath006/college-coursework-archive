import os
from celery.schedules import crontab
basedir = os.path.abspath(os.path.dirname(__file__))	# Absolute path of "application directory"

class Config():
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SECRET_KEY = "secret_key_OPEN_SESAME"
    DEBUG = False
    JWT_SECRET_KEY = "same_secret_key_OPEN_SESAME"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 120 # 2 minutes


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "lib_manage_sys.sqlite3")
    
    UPLOAD_FOLDER = os.path.join(basedir, "../frontend/public/book_files")
    DEBUG = True
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    CELERYBEAT_SCHEDULE = {
        'auto-revoke-access': {
            'task': 'application.tasks.Auto_Access_Revoke',
            'schedule': crontab(hour=7, minute=0),  # Runs every day at Morning 7 AM
        },
        'daily-reminders': {
            'task': 'application.tasks.Daily_Reminders',
            'schedule': crontab(hour=17, minute=0),  # Runs every day at Evening 5 PM
        },
        'monthly-report': {
            'task': 'application.tasks.Send_Monthly_Report',
            'schedule': crontab(minute=0, hour=8, day_of_month=1),  # Runs on Every Month 1st at Morning 8 AM
        },
    }
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 120 # 2 minutes

