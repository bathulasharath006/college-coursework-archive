from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_manager
from flask import current_app as app
from datetime import datetime as dt
from application.models import *
from application.validations import *
import bcrypt
import os


#-------------------------------------- Login Management -----------------------------------------
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(email):
    user = Users.query.get(email)
    if user:
        return user
    else:
        admin = Admins.query.get(email)
        return admin


#---------------------------- User Login credentials Validations ---------------------------------
@app.route("/login", methods=['POST'])
def logging_in():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        user = Users.query.filter_by(email=email).first()
        if user is None:
            return render_template('index.html',message="Wrong User ID<br>")
            
        elif check_password_bcrypt(password, user.hashed_passwd):
        	login_user(user, remember=True)
        	user = Users.query.filter_by(email=email).first()
        	id = user.id
        	return redirect(f'/logged_in/{id}')
        	        	
        else :
            message = f"Wrong Password<br>"
            return render_template('index.html', mail=email, message=message)


#------------------------------------- Logout the current user -------------------------------------
@app.route("/logout", methods=["GET"])
@login_required
def user_logout():

    logout_user()
    return redirect(url_for("index"))
    
    
#---------------------------- Admin Login credentials Validations ---------------------------------
@app.route("/admin_login", methods=['POST'])
def admin_logging_in():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        
        admin = Admins.query.filter_by(email=email).first()
        if admin is None:
            return render_template('index.html',message="Wrong User ID<br>")
            
        elif check_password_bcrypt(password, admin.hashed_passwd):
        	login_user(admin, remember=True)
        	return redirect(url_for("Admin_Logged_in"))
        	
        else:
            message = f"Wrong Password<br>"
            return render_template('index.html', mail=email, message=message)


#------------------------------------- Logout the current admin -------------------------------------
@app.route("/admin_logout", methods=["GET"])
@login_required
def admin_logout():

    logout_user()
    return redirect(url_for("index"))

