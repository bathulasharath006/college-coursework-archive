from flask import request, render_template, redirect, url_for
from datetime import datetime as dt
from flask import current_app as app
import bcrypt
import os

from application.models import * # Database Tables
from .validations import *  # Additional Security


#------------------------------ App Starting Page OR Index Page -----------------------------
@app.route("/")
def index():
    return render_template('index.html')

from application.controllers.login_controllers import *
from application.controllers.user_controllers import *
from application.controllers.admin_controllers import *

