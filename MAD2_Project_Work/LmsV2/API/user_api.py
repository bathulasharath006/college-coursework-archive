from flask import Flask, request, redirect, url_for, jsonify
from flask import current_app as app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from application.models import *
from application.validations import *
from main import cache
import os, ast, bcrypt
from datetime import datetime as dt, timedelta


# ===============================  USER / STUDENTS ROUTES  ========================================

#----------------------------------- User Login Credentials Validations ----------------------------
@app.route("/api/login", methods = ["POST"])
def logging_in():
    data = request.get_json()
    if data['email']== None or data['password']==None:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400

    email = data["email"].strip()
    password = data["password"].strip()
    user = Users.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Email ID not found in the database", "message": "User did not registered in the Library Portal"}), 404
    elif check_password_bcrypt(password, user.hashed_passwd):
        id = user.id
        user.last_login = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        
        access_token = create_access_token(identity=id, expires_delta=timedelta(days=1))
        return jsonify({'access_token': access_token, 'id': id}), 200
    else:
        return jsonify({ "error": "Unauthorized", "message": "Incorrect Password."}), 401


#---------------------------------- User Logged in page ------------------------------------------
@app.route('/api/logged_in/', methods=['GET'])
@jwt_required()
def user_logged_in_api():
    page = request.args.get('page', 1, type=int)
    return get_user_home_page_data(page)
#------------------------------- Function: Pagniation --------------------------------------------
@cache.memoize(60)
def get_user_home_page_data(page):
    books_pagination = Books.query.order_by(Books.added_on.desc()).paginate(page=page, per_page=8)
    books = books_pagination.items
    books_data = []
    for book in books:
        rating = ast.literal_eval(book.rating)
        fi = sum(rating.values())
        if fi == 0:
            avg_rating = 0
        else:
            fixi = sum(int(key) * value for key, value in rating.items())
            avg_rating = round(fixi / fi, 1)
        books_data.append({
            'sect': book.sect,
            'book_id': book.book_id,
            'book_name': book.book_name,
            'authors': book.authors,
            'synopsis': book.synopsis,
            'pages': book.pages,
            'added_on': book.added_on,
            'avg_rating': avg_rating
        }) # End of For Loop
    response = {
        'books': books_data,
        'page': books_pagination.page,
        'total_pages': books_pagination.pages,
        'has_next': books_pagination.has_next,
        'has_prev': books_pagination.has_prev,
        'next_num': books_pagination.next_num,
        'prev_num': books_pagination.prev_num,
    }
    return jsonify(response), 200


#--------------------- Function: Issue Date => Return Date ---------------------
def Get_Return_Date(issue_dt_in_txt):
	issue_dt = dt.strptime(issue_dt_in_txt, "%Y-%m-%d")
	rtn_dt = ( issue_dt + timedelta(days=7) ).strftime("%Y-%m-%d")
	return rtn_dt

#---------------------------- Student BackPack ---------------------------------
@app.route("/api/backpack/<int:id>")
@jwt_required()
def BackPack(id):
	user = Users.query.filter_by(id=id).first()
	books_borrowed = ast.literal_eval(user.books_borrowed)

	backpack = []
	for key in books_borrowed:
		backpack.append({
		'book_id': key,
		'issue_date': books_borrowed[key],
		'return_date': Get_Return_Date(books_borrowed[key])
		})
		
	response = { 'email': user.email, 'full_name': user.full_name, 'number': user.number, 'backpack': backpack }
	return jsonify(response),200


#--------------------------------- Show Book Details --------------------------------------------
@app.route("/api/book_details/<int:id>/<string:book_id>", methods=['GET'])
def Book_Details(id, book_id):
    book = Books.query.filter_by(book_id=book_id).first()
    rating = ast.literal_eval(book.rating)
    fi = sum(rating.values())
    if fi == 0:
        avg_rating = 0
    else:
        fixi = sum(key * value for key, value in rating.items())
        avg_rating = round((fixi / fi), 1)
    user = Users.query.filter_by(id=id).first()
    request = Requests.query.filter_by(email=user.email).all()
    try:
        books_borrowed = ast.literal_eval(user.books_borrowed)
        backpack = list(books_borrowed.keys())
    except:
        backpack=[]
    requests = [each.book_id for each in request]
    limit = len(backpack) + len(requests)
    
    response = {
        "book": {
            "sect": book.sect.title(),
            "book_id": book.book_id,
            "book_name": book.book_name,
            "authors": book.authors.title(),
            "synopsis": book.synopsis,
            "pages": book.pages,
            "added_on": book.added_on,
            "avg_rating": avg_rating
        },
        "backpack": backpack,
        "limit": limit,
        "requests": requests
    }
    return jsonify(response), 200


#---------------------------- Request Book Access ----------------------------------
@app.route("/api/requesting/<int:id>/<string:book_id>" )
def Request_Book(id, book_id):
	user = Users.query.filter_by(id=id).first()
	request = Requests( email=user.email, book_id=book_id )
	db.session.add(request)
	db.session.commit()
	return redirect(url_for('Book_Details', id=id, book_id=book_id ))


#------------------------------ User Returns Book ----------------------------------
@app.route("/api/return/<int:id>/<string:book_id>/<int:rate>" )
def Return_Book( id, book_id,rate):
	book = Books.query.filter_by(book_id=book_id).first()
	rating = ast.literal_eval(book.rating)
	rating[rate] = rating[rate] + 1 # Update Rating
	book.rating = str(rating)

	user = Users.query.filter_by(id=id).first()
	books_borrowed = ast.literal_eval(user.books_borrowed)
	del books_borrowed[book_id] # Remove Book from User
	user.books_borrowed = str(books_borrowed)
	
	pend_rtn = Pending_Returns.query.filter_by( email=user.email, book_id=book_id).first()
	transaction = Transactions.query.filter_by( email=user.email, book_id=book_id, issue_date=pend_rtn.issue_date ).first()
	return_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction.return_date = return_date # Add Return date to Transactions
	db.session.delete(pend_rtn) # Remove from Pending Returns
	db.session.commit()
	
	return jsonify({"message": "Book Returned"}), 200


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
@app.route('/api/search/<string:searchKey>/<string:searchQuery>')
def Search(searchKey, searchQuery):
    books = search_database(searchKey, searchQuery.strip())
    books_data = []
    for book in books:
        rating = ast.literal_eval(book.rating)
        fi = sum(rating.values())
        if fi == 0:
            avg_rating = 0
        else:
            fixi = sum(int(key) * value for key, value in rating.items())
            avg_rating = round(fixi / fi, 1)
        books_data.append({
            'sect': book.sect,
            'book_id': book.book_id,
            'book_name': book.book_name,
            'authors': book.authors,
            'synopsis': book.synopsis,
            'pages': book.pages,
            'added_on': book.added_on,
            'avg_rating': avg_rating
        }) # End of For Loop
    response = { 'books': books_data }
    return jsonify(response), 200
    
    
# =============================== ACCOUNT CRUD ROUTES  ======================================    

#----------------------------------- New User Registration --------------------------------
@app.route("/api/register", methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400

    email = data.get('email', '').strip()
    full_name = data.get('full_name', '').strip()
    number = str(data.get('number', '')).strip()
    create_password = data.get('create_password', '').strip()
    confirm_password = data.get('confirm_password', '').strip()
    key = data.get('key', '').strip()

    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({
        "error": "Account already exists.",
        "message": "Uh-oh! It looks like someone beat you to it. An account with this email already exists. Please try with a different email id"
        }), 409
    error = valid_register(email, full_name, number, create_password, confirm_password, key)
    if error:
        return jsonify({"error": "Form is overwritten.", "message": error}), 400

    hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
    new_user = Users(email=email, access_level=1, full_name=full_name,
           number=number, hashed_key=hashed_key, hashed_passwd=hashed_passwd,
           books_borrowed='{}', last_login = dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({ "succ_id": 1}), 201


#---------------------------- Get Student Details & Update Account Info  => Home page ----------------
@app.route("/api/update_student_details/<string:email>", methods=['GET', 'PUT'])
def updating_student_details(email):
    if request.method == 'GET':
        user = Users.query.filter_by( email=email.strip() ).first()
        if user is None:
            return jsonify({"error": "No data found", "message": "No details found for the given email id in the student database"}), 404
        if user.access_level != 1:
            return jsonify({"error": "No data found", "message": "No details found for the given email id in the student database"}), 404

        return jsonify({
            "email": user.email,
            "full_name": user.full_name,
            "number": user.number
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400
            
        email = data.get('email', '').strip()
        full_name = data.get('full_name', '').strip()
        number = data.get('number', '').strip()
        create_password = data.get('create_password', '').strip()
        confirm_password = data.get('confirm_password', '').strip()
        key = data.get('key', '').strip()

        user = Users.query.filter_by(email=email).first()
        if user:
            error = valid_register(email, full_name, number, create_password, confirm_password, key)
            if error:
                return jsonify({"message": error}), 400

            hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
            user.full_name = full_name
            user.number = number
            user.hashed_key = hashed_key
            user.hashed_passwd = hashed_passwd
            db.session.commit()
            
            return jsonify({ "succ_id": 2}), 200
        else:
            return jsonify({"message": "User not found"}), 404


#---------------------------- Get Student Details & Delete Account =>Home page ----------------
@app.route("/api/delete_student_account/<string:email>",  methods = ['GET', 'DELETE'])
def deleting_student_account(email):
	if request.method == 'GET':
		user = Users.query.filter_by(email=email).first()
		if user is None:
		    return jsonify({"error": "No data found", "message": "No details found for the given email id in the student database"}), 400
		if user.access_level != 1:
		    return jsonify({"error": "No data found", "message": "No details found for the given email id in the student database"}), 400
		
		return jsonify({ "email": user.email, "full_name": user.full_name,
		    "number": user.number }), 200
		    
	elif request.method == 'DELETE':
		user = Users.query.filter_by(email=email).first()
		if user :
			db.session.delete(user)
			db.session.commit()
			
			return jsonify({ "succ_id": 3}), 200
		else:
		    return jsonify({"message": "User not found"}), 404


#------------------------------------- Success Pages --------------------------------
@app.route("/api/success_page/<int:succ_id>")
def Success_Page(succ_id):
    if succ_id == 1:
        return jsonify({ "heading": "Registration Success!",
            "message": "Welcome aboard! Your library registration was a success. Knowledge is power, and it's at your fingertips. Login now to start your learning adventure.",
            "ending": "Congratulations",
            "url": '/' }), 200

    if succ_id == 2:
        return jsonify({ "heading": "Account Details Updated!",
            "message": "Libraries store the energy that fuels the imagination. They open up windows to the world and inspire us to explore and achieve, and contribute to improving our quality of life.",
            "ending": "Update Successful",
            "url": '/admin_home' }), 200

    if succ_id == 3:
        return jsonify({ "heading": "Account Deleted!",
            "message": "Sorry to see you Go!	 Come Back Soon.... 	Nothing is pleasanter than exploring a library.",
            "ending": "Deletion Successful", "url": '/admin_home' }), 200

    if succ_id == 4:
        return jsonify({ "heading": "Registration Success!",
            "message": "With Great Power, Comes Great Responsibility.",
            "ending": "Congratulations", "url": '/admin_home' }), 200

    if succ_id == 5:
        return jsonify({ "heading": "Account Details Updated!",
            "message": "Power cannot simply be enjoyed for its privileges alone but necessarily makes its holders morally responsible.",
            "ending": "Successfully", "url": '/admin_home' }), 200

    if succ_id == 6:
        return jsonify({ "heading": "Book Added!",
            "message": "Books are important for the mind, heart, and soul.",
            "ending": "More Books, More Knowledge", "url": '/admin_home' }), 200

    if succ_id == 7:
        return jsonify({ "heading": "Book Updated!",
            "message": "There is more treasure in books than in all the pirate's loot on Treasure Island.",
            "ending": "Walt Disney", "url": '/admin_home' }), 200

    if succ_id == 8:
        return jsonify({ "heading": "Book Deleted!",
            "message": "Reading is essential for those who seek above the ordinary.",
            "ending": "Jim Rohn", "url": '/admin_home' }), 200

