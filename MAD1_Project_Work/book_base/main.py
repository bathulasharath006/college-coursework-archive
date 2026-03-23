from flask import Flask
from flask_login import LoginManager
from application.configurations import LocalDevelopmentConfig
from application.models import * # Import Database Tables
import os

# -------------------------------- Logging ----------------------------------------
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
# ---------------------------------------------------------------------------------


app = None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key_OPEN_SESAME'
    if os.getenv('ENV', "development") == "production":
    	raise Exception("Currently NO production configurations is setup.")
    else:
    	print("Staring Local Development")
    	app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    app.app_context().push()
    return app

app = create_app()


# Import all the controllers where all the endpoint implementations and business
# logic are present.
from application.controller import *


if __name__ == '__main__':
  # Run the Flask app
  app.run(host = '0.0.0.0',port = 8080,debug = True)

