from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_caching import Cache
from application.configurations import LocalDevelopmentConfig
from application.models import * # Import Database Tables
from application import workers
from application import tasks
import os

# -------------------------------- Logging -------------------------------------
import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
# ------------------------------------------------------------------------------


def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
    	raise Exception("Currently NO production configurations is setup.")
    else:
    	print("Starting Local Development")
    	app.config.from_object(LocalDevelopmentConfig)
    CORS(app)
    jwt = JWTManager(app)
    jwt.init_app(app)
    db.init_app(app)
    app.app_context().push()
    

    celery = workers.celery
    celery.conf.update(
            broker_url = app.config["CELERY_BROKER_URL"],
            result_backend = app.config["CELERY_RESULT_BACKEND"],
            broker_connection_retry_on_startup = app.config["CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"],
            beat_schedule=app.config["CELERYBEAT_SCHEDULE"]
            )
    celery.Task = workers.ContextTask
    celery.set_default()
    app.app_context().push()
    
    cache = Cache(app)
    app.app_context().push()
    return app, jwt, celery, cache

app, jwt, celery, cache = create_app()


from API.user_api import *
from API.admin_api import *


if __name__ == '__main__':
  # Run the Flask app
  app.run(host = '0.0.0.0', port=5000, debug=True)

