import os
basedir = os.path.abspath(os.path.dirname(__file__))	# Absolute path of "application directory"

class Config():
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    DEBUG = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "lib_manage_sys.sqlite3")
    
    UPLOAD_FOLDER = os.path.join(basedir, "../static/book_files")
    DEBUG = True
    
