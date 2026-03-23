from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_manager
from datetime import datetime as dt, timedelta
from flask import current_app as app
import bcrypt
import os, ast

from application.models import *  # Database Tables
from application.validations import *  # Additional Security


# ===============================  USER / STUDENTS ROUTES  =========================================

#----------------------------- Function: Issue Date => Return Date ---------------------------------
def Get_Return_Date(issue_dt_in_txt):
	issue_dt = dt.strptime(issue_dt_in_txt, "%Y-%m-%d")
	rtn_dt = ( issue_dt + timedelta(days=7) ).strftime("%Y-%m-%d")
	return rtn_dt

#-------------------------- Function: Actions Before Removal of access -----------------------------
def Before_Return_Action( email, book_id):
	pend_rtn = Pending_Returns.query.filter_by( email=email, book_id=book_id).first()
	transaction = Transactions.query.filter_by( email=email, book_id=book_id, issue_date=pend_rtn.issue_date ).first()
	rtn_dt = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	
	transaction.return_date = rtn_dt # Add Return date to Transactions
	db.session.delete(pend_rtn) # Remove from Pending Returns

#---------------------------- Function: After 7 Days Remove Access  -------------------------------
def Auto_Access_Revoke():
	users = Users.query.all()
	for user in users:
		current_date = dt.now().strftime("%Y-%m-%d")
	
		if user.book_id1 is not None and user.book_id1 != "":
			return_date = Get_Return_Date( user.book1_issue_dt)
			if current_date > return_date:
				Before_Return_Action( user.email, user.book_id1)
				user.book_id1 = '' # Remove Book from user
				user.book1_issue_dt = ''

		if user.book_id2 is not None and user.book_id2 != "":
			return_date = Get_Return_Date( user.book2_issue_dt)
			if current_date > return_date:
				Before_Return_Action( user.email, user.book_id2)
				user.book_id2 = '' # Remove Book from user
				user.book2_issue_dt = ''

		if user.book_id3 is not None and user.book_id3 != "":
			return_date = Get_Return_Date( user.book3_issue_dt)
			if current_date > return_date:
				Before_Return_Action( user.email, user.book_id3)
				user.book_id3 = '' # Remove Book from user
				user.book3_issue_dt = ''

		if user.book_id4 is not None and user.book_id4 != "":
			return_date = Get_Return_Date( user.book4_issue_dt)			
			if current_date > return_date:
				Before_Return_Action( user.email, user.book_id4)
				user.book_id4 = '' # Remove Book from user
				user.book4_issue_dt = ''
				
		if user.book_id5 is not None and user.book_id5 != "":
			return_date = Get_Return_Date( user.book5_issue_dt)			
			if current_date > return_date:
				Before_Return_Action( user.email, user.book_id5)
				user.book_id5 = '' # Remove Book from user
				user.book5_issue_dt = ''
				
		db.session.commit() # Commit for each user.
#--------------------------------------------------------------------------------------------------


#---------------------------------- User Logged in page -------------------------------------------
@app.route('/logged_in/<int:id>')
@login_required
def User_Logged_in(id):
	
	Auto_Access_Revoke()
	page = request.args.get('page', 1, type=int)
	return render_user_home_page(id, page)
#------------------------------- Function: Pagniation --------------------------------------------
def render_user_home_page(id, page):
	
	books = Books.query.order_by(Books.added_on.desc()).paginate(page=page, per_page=8)
	
	avg_rating=[] # Average Ratings 
	for book in books:
		rating = ast.literal_eval(book.rating)
		fi = sum(rating.values())
		if fi == 0:
			avg_rating.append(0)
		else:
			fixi=0
			for key, value in rating.items():
				fixi += key*value
			avg_rating.append( round( (fixi/fi),1) )
		
	return render_template('/user_templates/user_home_page.html', books=books, id=id, avg_rating=avg_rating )
#--------------------------------------------------------------------------------------------------


#--------------------------------- Show Book Details --------------------------------------------
@app.route("/book_details/<int:id>/<string:book_id>" )
def Book_Details(id, book_id):
	
	book = Books.query.filter_by(book_id=book_id).first()

	rating = ast.literal_eval(book.rating)
	fi = sum(rating.values())
	if fi == 0:
		avg_rating=0
	else:
		fixi=0
		for key, value in rating.items():
			fixi += key*value
		avg_rating=  round( (fixi/fi),1) 


	user = Users.query.filter_by(id=id).first()
	request = Requests.query.filter_by(email=user.email).all()
	
	backpack = []
	if user.book_id1 is not None and user.book_id1 != "":
		backpack.append(user.book_id1)
	if user.book_id2 is not None and user.book_id2 != "":
		backpack.append(user.book_id2)
	if user.book_id3 is not None and user.book_id3 != "":
		backpack.append(user.book_id3)
	if user.book_id4 is not None and user.book_id4 != "":
		backpack.append(user.book_id4)
	if user.book_id5 is not None and user.book_id5 != "":
		backpack.append(user.book_id5)
		
	requests = []
	for each in request:
		requests.append(each.book_id)
	limit = len(backpack) + len(requests)
	
	return render_template('/user_templates/user_book_details.html', book=book, id=id,
	           backpack=backpack, limit=limit, requests=requests, avg_rating=avg_rating )
#-----------------------------------------------------------------------------------


#---------------------------- Request Book Access ----------------------------------
@app.route("/requesting/<int:id>/<string:book_id>" )
def Request_Book(id, book_id):

	user = Users.query.filter_by(id=id).first()
	request = Requests( email=user.email, book_id=book_id )
	db.session.add(request)
	db.session.commit()
	return redirect(url_for('Book_Details', id=id, book_id=book_id ))


#---------------------------- User Returns Book ----------------------------------
@app.route("/return/<int:id>/<string:book_id>/<string:page>" , methods = [ "GET", "POST"] )
def Return_Book( id, book_id, page):

	if request.method == "POST":
		rate = int(request.form['rate'])
	else:
		rate = 4

	book = Books.query.filter_by(book_id=book_id).first()
	rating = ast.literal_eval(book.rating)
	rating[rate] = rating[rate] + 1 # Update Rating
	book.rating = str(rating)

	user = Users.query.filter_by(id=id).first()
	if user.book_id1 == book_id : # Remove Book from User
		user.book_id1 = ''
		user.book1_issue_dt = ''
		
	elif user.book_id2 == book_id :
		user.book_id2 = ''
		user.book2_issue_dt = ''
	
	elif user.book_id3 == book_id :
		user.book_id3 = ''
		user.book3_issue_dt = ''
	
	elif user.book_id4 == book_id :
		user.book_id4 = ''
		user.book4_issue_dt = ''
	
	elif user.book_id5 == book_id :
		user.book_id5 = ''
		user.book5_issue_dt = ''
	
	pend_rtn = Pending_Returns.query.filter_by( email=user.email, book_id=book_id).first()
	transaction = Transactions.query.filter_by( email=user.email, book_id=book_id, issue_date=pend_rtn.issue_date ).first()
	return_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction.return_date = return_date # Add Return date to Transactions
	db.session.delete(pend_rtn) # Remove from Pending Returns
	db.session.commit()
	
	if page == 'bk_dtls':
		return redirect(url_for('Book_Details', id=id, book_id=book_id ))
	elif page == 'backpack':
		return redirect(url_for('User_Backpack', id=id ))
	else:
		return redirect('/')


#------------------------------------- User's Backpack ----------------------------------------
@app.route("/user/backpack/<int:id>")
def User_Backpack(id):
	user = Users.query.filter_by(id=id).first()

	backpack = []
	if user.book_id1 is not None and user.book_id1 != "":
		backpack.append(( user.book_id1, user.book1_issue_dt, Get_Return_Date(user.book1_issue_dt) ))

	if user.book_id2 is not None and user.book_id2 != "":
		backpack.append((user.book_id2, user.book2_issue_dt, Get_Return_Date(user.book2_issue_dt) ))

	if user.book_id3 is not None and user.book_id3 != "":
		backpack.append((user.book_id3, user.book3_issue_dt, Get_Return_Date(user.book3_issue_dt) ))

	if user.book_id4 is not None and user.book_id4 != "":
		backpack.append((user.book_id4, user.book4_issue_dt, Get_Return_Date(user.book4_issue_dt) ))

	if user.book_id5 is not None and user.book_id5 != "":
		backpack.append((user.book_id5, user.book5_issue_dt, Get_Return_Date(user.book5_issue_dt) ))
	
	return render_template('/user_templates/user_backpack.html', user=user, backpack=backpack )


#------------------------- New User Registration --------------------------------------------
@app.route("/register", methods = [ 'GET', 'POST'])
def registering():
    if request.method == 'POST':
        email = request.form['email'].strip()
        full_name = request.form['full_name'].strip().upper()
        number = request.form['number'].strip()
        create_password = request.form['create_password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        key = request.form['key'].strip()
        
        user = Users.query.filter_by(email=email).first()
        if user :
            error = "Uh-oh! It looks like someone beat you to it. An account with this email already exists.<br> Please try with different email id."
            return render_template("registration.html",error=error)
        else:
            error = valid_register(email, full_name, number, create_password, confirm_password, key)
            if error :
                return render_template('registration.html',error=error)
            
            hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
            user = Users(email=email, full_name=full_name, number=number, hashed_key=hashed_key, hashed_passwd=hashed_passwd)
            db.session.add(user)
            db.session.commit()
        
        heading = "Registration Success!"
        message = "Welcome aboard! Your library registration was a success. Knowledge is power, and it's at your fingertips. Login now to start your learning adventure."
        ending = "Congratulations"
        url='/'
        return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
    else:
        return render_template('registration.html')


#---------------- Function: perform search based on selected radio button -----------------
def search_database(searchKey, searchQuery):
    if searchKey == 'book_name':
        results = Books.query.filter(Books.book_name.like('%' + searchQuery + '%')).all()
    elif searchKey == 'sect':
        results = Books.query.filter(Books.sect.like('%' + searchQuery + '%')).all()
    elif searchKey == 'authors':
        results = Books.query.filter(Books.authors.like('%' + searchQuery + '%')).all()
        
    elif searchKey == 'all':
        results = Books.query.filter(
        (Books.book_id.like('%' + searchQuery + '%')) |
        (Books.book_name.like('%' + searchQuery + '%')) |
        (Books.sect.like('%' + searchQuery + '%')) |
        (Books.authors.like('%' + searchQuery + '%'))
    ).all()
    return results


#---------------------------- Search Functionality -------------------------
@app.route('/search/<int:id>')
def Search(id):
	searchKey = request.args.get('searchKey', 'all')
	searchQuery = request.args.get('searchQuery').strip()
	
	books = search_database(searchKey, searchQuery)
	return render_template('/user_templates/user_search_pg.html', books=books, id=id)


#---------------------------- Get Student Details & Update Account Info  => Home page ----------------
@app.route("/update_student_details",  methods = ['GET', 'POST'])
def Updating_student_details():

	if request.method == 'GET':
		email = request.args.get('GetDetails', '').strip()
		
		user = Users.query.filter_by(email=email).first()
		if user is None:
			noDetailsMessage = 'No details found for the given email'
			return render_template('update_details.html', role="Student", email=email, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('update_details.html', role="Student", email=user.email, full_name=user.full_name, number=user.number)

	elif request.method == 'POST':
		email = request.form['email'].strip()
		full_name = request.form['full_name'].strip().upper()
		number = request.form['number'].strip()
		create_password = request.form['create_password'].strip()
		confirm_password = request.form['confirm_password'].strip()
		key = request.form['key'].strip()
		
		user = Users.query.filter_by(email=email).first()
		if user :
			error=''
			error = valid_register(email, full_name, number, create_password, confirm_password, key)
			if error :
				return render_template('update_details.html', role="Student", email=email, noDetailsMessage=error)
			
			hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
			user.full_name = full_name
			user.number = number
			user.hashed_key = hashed_key
			user.hashed_passwd = hashed_passwd
			db.session.commit()
				
			heading = "Account Details Updated!"
			message = "Libraries store the energy that fuels the imagination. They open up windows to the world and inspire us to explore and achieve, and contribute to improving our quality of life."
			ending = "Update Successful"
			url='/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
		else:
			return render_template('index.html')


#---------------------------- Get Student Details & Delete Account =>Home page ----------------
@app.route("/delete_student_account",  methods = ['GET', 'POST'])
def deleting_student_account():
	if request.method == 'GET':
		role = "Student"
		email = request.args.get('GetDetails', '').strip()
		
		user = Users.query.filter_by(email=email).first()
		if user is None:
			noDetailsMessage = 'No details found for the given email'
			return render_template('delete_account.html', role=role, email=email, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('delete_account.html', role=role, email=user.email, full_name=user.full_name, number=user.number)
		    
	elif request.method == 'POST':
		email = request.form['email'].strip()
		
		user = Users.query.filter_by(email=email).first()
		if user :
			db.session.delete(user)
			db.session.commit()

			heading = "Account Deleted!"
			message = "Sorry to see you Go!	 Come Back Soon.... 	Nothing is pleasanter than exploring a library."
			ending = "Delete Successful"
			url='/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
		else:
			return render_template('index.html')


#----------------------------- Forgot Password then Reset it ----------------------------------
@app.route("/forgot_passwd", methods = ['GET', 'POST'])
def hpassword_reset():
    if request.method == 'POST':
        email = request.form['email'].strip()
        key = request.form['key'].strip()
        create_password = request.form['create_password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        
        user = Users.query.filter_by(email=email).first()
        if user is None:
        	errorMessage = 'Wrong User ID<br>'
        	return render_template('forgot_password.html', errorMessage=errorMessage )
        	
        elif check_password_bcrypt(key, user.hashed_key):
        	hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
        	user.hashed_passwd = hashed_passwd
        	db.session.commit()
        	
        	heading = "Password Updated!"
        	message = "Welcome Back ...  Everything you need for better future and success has already been written. And guess what? All you have to do is go to the library."
        	ending = "Update Successful"
        	url='/'
        	return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
        	
        else:
        	errorMessage = 'Secret Key Didn\'t Match<br>'
        	return render_template('forgot_password.html', errorMessage=errorMessage )
    else:
    	return render_template('forgot_password.html')
        
        

