from flask import Flask, request, jsonify, send_file
from flask import current_app as app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from application.models import *
from application.validations import *
from application.tasks import export_csv
from main import cache
import os, ast, bcrypt
from datetime import datetime as dt, timedelta, date
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from collections import Counter, defaultdict


# ===============================  ADMIN / LIBRARIAN ROUTES  =======================================

#---------------------------------- Admin Login credentials Validations -----------------------------
@app.route("/api/adm_login", methods = ["POST"])
def admin_logging_in():
    data = request.get_json()
    if data['email']== None or data['password']==None:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400

    email = data["email"].strip()
    password = data["password"].strip()
    admin = Users.query.filter_by(email=email).first()
    if admin is None:
        return jsonify({"error": "Email ID not found in the database", "message": "User did not registered in the Library Portal."}), 404
    elif check_password_bcrypt(password, admin.hashed_passwd):
        if admin.access_level == 0:            
            access_token = create_access_token(identity=admin.id, expires_delta=timedelta(days=1))
            admin.last_login = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            db.session.commit()
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({ "error": "Unauthorized", "message": "You are not authorized to access the Librarian Page."}), 403
    else:
        return jsonify({ "error": "Unauthorized", "message": "Incorrect Password."}), 401


#------------------------------ Admin Home Page --------------------------------
@app.route('/api/admin_home')
@jwt_required()
def Admin_Home():
    requests = Requests.query.all()
    data = []
    for req in requests:
        data.append({ 
        'email': req.email,
        'book_id': req.book_id
        })
    return jsonify(data),200


#----------------------- Function: Issue Date => Return Date -------------------
def Get_Return_Date(issue_dt_in_txt):
	issue_dt = dt.strptime(issue_dt_in_txt, "%Y-%m-%d")
	rtn_dt = ( issue_dt + timedelta(days=7) ).strftime("%Y-%m-%d")
	return rtn_dt


#------------------------- Admin views Student Details -------------------------
@app.route("/api/admin/student_details/<string:email>")
@jwt_required()
def Admin_View_Student_Details(email):
	user = Users.query.filter_by(email=email).first()
	books_borrowed = ast.literal_eval(user.books_borrowed)

	backpack = []
	for key in books_borrowed:
		backpack.append({
		'book_id': key,
		'issue_date': books_borrowed[key],
		'return_date': Get_Return_Date(books_borrowed[key])
		})
		
	response = { 'email': email, 'full_name': user.full_name, 'number': user.number, 'backpack': backpack }
	return jsonify(response),200


#--------------------------- Admin Accepts Book Request ----------------------------
@app.route("/api/admin/accept_request/<string:email>/<string:book_id>" )
def Accept_Request(email, book_id):
	request = Requests.query.filter_by(email=email, book_id=book_id).first()
	db.session.delete(request) # Remove from Requests Table
	
	issue_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction = Transactions( email=email, book_id=book_id, action="Accept", issue_date=issue_date )
	db.session.add(transaction)  # Add Transaction into dataBase
	
	pend_rtns = Pending_Returns(email=email, book_id=book_id, issue_date=issue_date)
	db.session.add(pend_rtns) # Add Book into Pending Returns

	user = Users.query.filter_by(email=email).first() # Add Book into Users Table
	books_borrowed = ast.literal_eval(user.books_borrowed)
	books_borrowed[book_id]= issue_date.split(' ')[0]
	user.books_borrowed = str(books_borrowed)
		
	db.session.commit()
	return jsonify({"message": "Book Issued"}), 200


#--------------------------- Admin Rejects Book Request ------------------------
@app.route("/api/admin/reject_request/<string:email>/<string:book_id>" )
def Reject_Request(email, book_id):
	issue_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction = Transactions( email=email, book_id=book_id, action="Reject", issue_date=issue_date )
	db.session.add(transaction)  # Add Transaction into dataBase
	
	request = Requests.query.filter_by(email=email, book_id=book_id).first()
	db.session.delete(request) # Remove from Requests Table
	db.session.commit()
	return jsonify({"message": "Book Rejected"}), 200


#--------------------------- Admin Revoke's Book Access ------------------------
@app.route("/api/admin/revoke/<string:email>/<string:book_id>" )
def Revoke_Book_Access( email, book_id):
	user = Users.query.filter_by(email=email).first()
	books_borrowed = ast.literal_eval(user.books_borrowed)
	del books_borrowed[book_id] # Remove Book from User
	user.books_borrowed = str(books_borrowed)
	
	pend_rtn = Pending_Returns.query.filter_by( email=email, book_id=book_id).first()
	transaction = Transactions.query.filter_by( email=email, book_id=book_id, issue_date=pend_rtn.issue_date ).first()
	return_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction.return_date = return_date # Add Return date to Transactions
	
	db.session.delete(pend_rtn) # Remove from Pending Returns
	db.session.commit()
	return jsonify({"message": "Book Access Revoked"}), 200


#--------------------------- Admin checks Pending Returns ----------------------
@app.route("/api/admin/pending_returns" )
@jwt_required()
def Pending_Books_List():
	rows = Pending_Returns.query.all()
	pnd_rtns = []
	for each in rows:
		pnd_rtns.append({
		'email': each.email,
		'book_id': each.book_id,
		'issue_date': each.issue_date,
		'return_date': Get_Return_Date(each.issue_date.split()[0])
		})
	
	return jsonify(pnd_rtns), 200


# ========================== STATISTICS ROUTES  ================================

basedir = os.path.abspath(os.path.dirname(__file__))
PLOTS_DIR = os.path.join(basedir, "../db_directory/plots/")
#------------------------------ Charts Home Page -------------------------------
@app.route("/api/statistics" )
def Statistics():
	trans = Transactions.query.all()
	
	#---- Top 10 Popular Books ----#
	book_ids = [ tran.book_id for tran in trans]	
	books_dict = Counter(book_ids)
	book_ids = dict(sorted(books_dict.items(), key=lambda item: item[1], reverse=True))
	reversed_10_books = dict(list(book_ids.items())[:10])
	first_10_books = dict(list(reversed_10_books.items())[::-1])
	
	x = list(first_10_books.keys())
	y = list(first_10_books.values())
	cmap = plt.cm.get_cmap('plasma')
	max_value = max(y)
	normalized_values = [each_y / max_value for each_y in y]
	
	plt.figure(figsize=(9, 6))		
	bars = plt.barh(x, y, height=0.5, color=cmap(normalized_values))
	plt.bar_label(bars )
	plt.tight_layout(pad=2.0)
	plt.savefig(PLOTS_DIR + 'popular_books.png', bbox_inches='tight')
	plt.close()
	
	#---- Top 10 Books Borrowers ----#
	emails = [ tran.email.strip('@gmail.com') for tran in trans]	
	emails_dict = Counter(emails)
	emails = dict(sorted(emails_dict.items(), key=lambda item: item[1]))
	first_10_borrowers = dict(list(emails.items())[:10])
	
	x = list(first_10_borrowers.keys())
	y = list(first_10_borrowers.values())
	cmap = plt.cm.get_cmap('gist_rainbow')
	max_value = max(y)
	normalized_values = [each_y / max_value for each_y in y]
	
	plt.figure(figsize=(9, 6))
	bars = plt.bar(x, y, width= 0.5, color=cmap(normalized_values))
	plt.bar_label(bars )
	plt.xticks(rotation=45)
	plt.savefig(PLOTS_DIR + 'popular_borrowers.png', bbox_inches='tight')
	plt.close()
	
	#---- Past 10 days "Accept" and "Reject" Counts on each date ---#
	days_count=10
	today = dt.today()
	past_n_days = today - timedelta(days=days_count)
	transactions = Transactions.query.filter(
	       Transactions.issue_date >= past_n_days.strftime('%Y-%m-%d')).all()
	
	# Initialize a dictionary with the last 10 days.
	# This ensures each date has an entry in the summary.
	summary = defaultdict(lambda: { 'Accept': 0, 'Reject': 0})
	for i in range(days_count):
	    date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
	    summary[date]  
	
	for transaction in transactions:  # Populate the dictionary with transaction counts
	    date = dt.strptime(transaction.issue_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
	    summary[date][transaction.action] += 1
	    
	sorted_summary = dict(sorted(summary.items(), key=lambda item: item[0]))
	
	plt.figure(figsize=(20, 6))
	dates = list(sorted_summary.keys())
	accept_counts = [sorted_summary[date]['Accept'] for date in dates]
	reject_counts = [sorted_summary[date]['Reject'] for date in dates]
	
	plt.scatter(dates, accept_counts, color='green', label='Accept')
	for i, count in enumerate(accept_counts):
	    plt.annotate(str(count), (dates[i], count), textcoords="offset points",
	         xytext=(10, 10), ha='center')
	
	plt.scatter(dates, reject_counts, color='red', label='Reject')
	for i, count in enumerate(reject_counts):
	    plt.annotate(str(count), (dates[i], count), textcoords="offset points", xytext=(-10, -10), ha='center')
	
	plt.plot(dates, accept_counts, color='green', linestyle='-', linewidth=1)
	plt.plot(dates, reject_counts, color='red', linestyle='-', linewidth=1)
	plt.xticks(rotation=45)
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.savefig(PLOTS_DIR + 'scatter.png', bbox_inches='tight')
	plt.close()
	
	#---- Section Wise Bar Chart ----#
	books = Books.query.all()
	sections = [ book.sect for book in books]
	sects_dict = Counter(sections)
	
	x = list(sects_dict.keys())
	y = list(sects_dict.values())
	cmap = plt.cm.get_cmap('plasma')
	max_value = max(y)
	normalized_values = [each_y / max_value for each_y in y]
	
	plt.figure(figsize=(14, 7))
	bars = plt.bar(x, y, color=cmap(normalized_values))
	plt.bar_label(bars )
	plt.savefig(PLOTS_DIR + 'sections.png', bbox_inches='tight')
	plt.close()
	
	return jsonify({ "message": "Successful" }), 200
	
	
#------------------------------ BookWise Statistics ----------------------------
@app.route("/api/bookStats/<string:book_id>")
@jwt_required()
def Book_Statistics(book_id):
    book_id=book_id.upper()
    book = Books.query.filter_by(book_id=book_id).first()
    if book is None:
        return jsonify({"error": "No data found", "book_id": None }), 404
        
    # Pie Chart for Accept vs Reject
    accept_count = Transactions.query.filter_by(book_id=book_id, action='Accept').count()
    reject_count = Transactions.query.filter_by(book_id=book_id, action='Reject').count()
    counts = [accept_count, reject_count]
    labels = ['Accept', 'Reject']
    colors = ['#08df12', '#f51009']
    
    plt.figure(figsize=(5, 5))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')
    plt.text(1, 1, f'Accept: {accept_count}\nReject: {reject_count}',
           horizontalalignment='right', verticalalignment='top')
    plt.savefig(PLOTS_DIR + 'Accept_Vs_Reject.png', bbox_inches='tight')
    plt.close()
    
    # Bar Chart for Ratings
    rating = ast.literal_eval(book.rating)
    x = list(rating.keys())
    y = list(rating.values())
    colors = {1: '#f44336', 2: '#ffff00', 3: '#ff9800', 4: '#2196F3', 5: '#04AA6D'}
    
    bars = plt.bar(x, y, width=0.4)
    for bar, key in zip(bars, x):
        bar.set_color(colors[key])
    plt.bar_label(bars)
    plt.savefig(PLOTS_DIR + 'ratings.png', bbox_inches='tight')
    plt.close()

    return jsonify({ "message": "Successful", "book_id": book_id }), 200
	
	
#-------------------------------- Transactions Page ---------------------------------------
@app.route("/api/transactions/")
@jwt_required()
def TransactionsPage():
	page = request.args.get('page', 1, type=int)
	trans_pagination = Transactions.query.order_by(Transactions.id.desc()).paginate(page=page, per_page=16)
	trans = trans_pagination.items
	trans_data = []
	for each in trans:
	    trans_data.append({
	          'id': each.id,
	          'email': each.email,
	          'book_id': each.book_id,
	          'action': each.action,
	          'issue_date': each.issue_date,
	          'return_date': each.return_date
	          })
	          
	response = {
	      'entries': trans_data,
	      'page': trans_pagination.page,
	      'total_pages': trans_pagination.pages,
	      'has_next': trans_pagination.has_next,
	      'has_prev': trans_pagination.has_prev,
	      'next_num': trans_pagination.next_num,
	      'prev_num': trans_pagination.prev_num,
	      }
	      
	return jsonify(response), 200


# ------------------- User Triggered Async Job - Export as CSV -----------------
@app.route("/api/export_csv", methods=['POST'])
def trigger_export_csv():
    # Trigger the Celery task
    task = export_csv.apply_async()

    return jsonify({"task_id": task.id, "status": "Processing"}), 202

@app.route("/api/get_csv/<task_id>", methods=['GET'])
def get_csv(task_id):
    task = export_csv.AsyncResult(task_id)
    
    if task.state == 'SUCCESS':
        return jsonify({"status": "Success", "file_url": "transactions.csv"})
    elif task.state == 'PENDING' or task.state == 'PROGRESS':
        return jsonify({"status": "Processing"})
    else:
        return jsonify({"status": "Failed"}), 500
# ------------------------------------------------------------------------------


# =============================== ACCOUNT CRUD ROUTES  ======================================

#------------------------- New Librarian Registration ---------------------------------------
@app.route("/api/registerLibrarian", methods = ['POST'])
def registering_admin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400

    email = data.get('email', '').strip()
    full_name = data.get('full_name', '').strip()
    number = str(data.get('number', '')).strip()
    create_password = data.get('create_password', '').strip()
    confirm_password = data.get('confirm_password', '').strip()
    key = data.get('key', '').strip()

    admin = Users.query.filter_by(email=email).first()
    if admin:
        return jsonify({
        "error": "Account already exists.",
        "message": "An account with this email already exists. Log in or try registering with another email"
        }), 409
    error = valid_register(email, full_name, number, create_password, confirm_password, key)
    if error:
        return jsonify({"error": "Form is overwritten.", "message": error}), 400

    hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
    new_admin = Users(email=email, access_level=0, full_name=full_name,
         number=number, hashed_key=hashed_key, hashed_passwd=hashed_passwd,
         books_borrowed='{}', last_login = dt.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({ "succ_id": 4}), 201


#---------------------------- Get Librarian Details & Update Account Info  => Home page ----------------
@app.route("/api/update_librarian_details/<string:email>",  methods = ['GET', 'PUT'])
def Updating_librarian_details(email):
	if request.method == 'GET':
	    admin = Users.query.filter_by( email=email.strip() ).first()
	    if admin is None or admin.access_level != 0:
	        return jsonify({"error": "No data found", "message": "No details found for the given email id in the librarian database"}), 404
	        
	    return jsonify({ "email": admin.email, "full_name": admin.full_name,
	        "number": admin.number }), 200
	        
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
	    
	    admin = Users.query.filter_by(email=email).first()
	    if admin:
	        error = valid_register(email, full_name, number, create_password, confirm_password, key)
	        if error:
	            return jsonify({"message": error}), 400
	        
	        hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
	        admin.full_name = full_name
	        admin.number = number
	        admin.hashed_key = hashed_key
	        admin.hashed_passwd = hashed_passwd
	        db.session.commit()
	        
	        return jsonify({ "succ_id": 5}), 200
	    else:
	        return jsonify({"message": "User not found"}), 404


#---------------------------- Get Librarian Details & Delete Account => Home page ----------------
@app.route("/api/delete_librarian_details/<string:email>",  methods = ['GET', 'DELETE'])
def deleting_admin_account(email):
	if request.method == 'GET':
		user = Users.query.filter_by(email=email).first()
		if user is None:
		    return jsonify({"error": "No data found", "message": "No details found for the given email id in the student database"}), 400
		if user.access_level != 0:
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


# ===============================  BOOKS CRUD ROUTES  ======================================

#---------------------------------- Add New Book -------------------------------------------
@app.route("/api/admin_add_book", methods=['POST'])
def admin_adding_book():
    if request.method == 'POST':
        sect = request.form['sect'].strip().upper()
        book_id = request.form['book_id'].strip().upper()
        book_name = request.form['book_name'].strip()
        authors = request.form['authors'].strip().upper()
        synopsis = request.form['synopsis'].strip()
        pages = request.form['pages'].strip()
        cover_pg = request.files['image']
        pdf_file = request.files['pdfFile']
        added_on = dt.now().strftime("%Y-%m-%d")

        book = Books.query.filter_by(book_id=book_id).first()
        if book:
            return jsonify({"error": 409, "message": "Book already exists"}), 409

        error = valid_addBook(sect, book_id, book_name, authors, synopsis, cover_pg, pdf_file, added_on)
        if error:
            return jsonify({"error": 400, "message": error}), 400

        # Rename files based on book ID
        image_filename = f'{book_id}.jpg'
        pdf_filename = f'{book_id}.pdf'

        # Save the files to the specified upload folder
        cover_pg.save(app.config['UPLOAD_FOLDER'] + '/' + image_filename)
        pdf_file.save(app.config['UPLOAD_FOLDER'] + '/' + pdf_filename)

        rating = '{ 1:0, 2:0, 3:0, 4:0, 5:0 }'
        book = Books(sect=sect, book_id=book_id, book_name=book_name, authors=authors,
                     synopsis=synopsis, pages=pages, added_on=added_on, rating=rating)
        
        # Add book_id into Section Table
        section = Section.query.filter_by(section_name=sect).first()
        if section:
            books_ids = ast.literal_eval(section.books_ids)
            books_ids.append(book_id)
            section.books_ids = str(books_ids)
        
        db.session.add(book)
        db.session.commit()
        cache.delete_memoized(get_user_home_page_data)

        return jsonify({ "succ_id": 6}), 201


#-------------------------------- Update Book ----------------------------------
@app.route("/api/admin_update_book/<string:book_id>",  methods = ['GET', 'PUT'])
def admin_updates_book(book_id):
    if request.method == 'GET':
        book = Books.query.filter_by(book_id=book_id.upper()).first()
        if book is None:
            return jsonify({"error": "No data found", "message": "No details found for the given book id"}), 404
            
        response = {
                "sect": book.sect.title(),
                "book_id": book.book_id,
                "book_name": book.book_name,
                "authors": book.authors.title(),
                "synopsis": book.synopsis,
                "pages": book.pages,
                "added_on": book.added_on,
        }
        return jsonify(response), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400

        sect = data.get('sect').strip().upper()
        book_name = data.get('book_name').strip()
        authors = data.get('authors').strip().upper()
        synopsis = data.get('synopsis').strip()
        pages = data.get('pages')

        book = Books.query.filter_by(book_id=book_id.upper()).first()
        if book:
            book.sect = sect
            book.book_name = book_name
            book.authors = authors
            book.synopsis = synopsis
            book.pages = pages
            db.session.commit()

        return jsonify({ "succ_id": 7}), 201


#---------------- Function: Remove book pdf and image from Storage -------------
def removeBook(book_id):
    image_filename = f'{book_id}.jpg'
    pdf_filename = f'{book_id}.pdf'
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    
    os.remove(image_path)
    os.remove(pdf_path)
    return True
#-------------------------------- Delete Book ----------------------------------
@app.route("/api/admin_delete_book/<string:book_id>",  methods = ['GET', 'DELETE'])
def admin_deletes_book(book_id):
    book_id=book_id.upper()
    if request.method == 'GET':
        book = Books.query.filter_by(book_id=book_id).first()
        if book is None:
            return jsonify({"error": "No data found", "message": "No details found for the given book id"}), 404
            
        response = {
                "sect": book.sect.title(),
                "book_id": book.book_id,
                "book_name": book.book_name,
                "authors": book.authors.title(),
                "synopsis": book.synopsis,
                "pages": book.pages,
                "added_on": book.added_on,
        }
        return jsonify(response), 200

    elif request.method == 'DELETE':
        book = Books.query.filter_by(book_id=book_id).first()
        if book and removeBook(book_id):
            # Removing Book_ID from Sections Table
            section = Section.query.filter_by(section_name=book.sect).first()
            books_ids = ast.literal_eval(section.books_ids)
            books_ids.remove(book_id)
            section.books_ids = str(books_ids)
            
            db.session.delete(book)
            db.session.commit()
            cache.delete_memoized(get_user_home_page_data)
            
            return jsonify({ "succ_id": 8}), 200
        else:
            return jsonify({"message": "Book not found"}), 404


#--------------------------------- Get Book Details --------------------------------------------
@app.route("/api/adm_book_details/<string:book_id>", methods=['GET'])
def Admin_Book_Details(book_id):
    book = Books.query.filter_by(book_id=book_id.upper()).first()
    if book is None:
        return jsonify({"error": "No data found", "message": "No details found for the given book id"}), 404
        
    rating = ast.literal_eval(book.rating)
    fi = sum(rating.values())
    if fi == 0:
        avg_rating = 0
    else:
        fixi = sum(key * value for key, value in rating.items())
        avg_rating = round((fixi / fi), 1)
    response = {
            "sect": book.sect.title(),
            "book_id": book.book_id,
            "book_name": book.book_name,
            "authors": book.authors.title(),
            "synopsis": book.synopsis,
            "pages": book.pages,
            "added_on": book.added_on,
            "avg_rating": avg_rating
    }
    return jsonify(response), 200
    
    
#----------------------------- Get Sections Details ----------------------------
@app.route("/api/getSectionDetails")
def SectionsDetails():
    sects = Section.query.all()
    data = []    
    for each in sects:
        data.append({
              'sect_name': each.section_name,
              'sect_desc': each.section_description,
              'create_date': each.section_created_date,
              'books_ids': ast.literal_eval(each.books_ids)
              })
    return jsonify(data), 200
    
    
#-------------------------------- Add Section ----------------------------------
@app.route("/api/addSection", methods = ['POST' ])
def AddingSection():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400
        
    section_name = data.get('section_name', '').strip().upper()
    section_description = data.get('section_description', '').strip()
    section_created_date = dt.now().strftime("%Y-%m-%d")
    books_ids = '[ ]'
    
    section = Section.query.filter_by(section_name=section_name).first()
    if section:
        return jsonify({
        "error": "Section already exists.",
        "message": f"{section_name} already exists. Try different section name."
        }), 409
    section = Section(section_name=section_name, section_description=section_description,
           section_created_date=section_created_date, books_ids=books_ids)

    db.session.add(section)
    db.session.commit()
    return jsonify({ "message": "New Section Added"}), 201
    
    
#------------------------------ Update Section ---------------------------------
@app.route("/api/updateSection/<string:sect_name>", methods = ['PUT'])
def UpdatingSection(sect_name):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided", "message": "No input data provided"}), 400
        
    section_name_updated = data.get('section_name', '').strip().upper()
    section_description_updated = data.get('section_description', '').strip()
    
    section = Section.query.filter_by(section_name=sect_name).first()
    if section:
        # Update the section
        section.section_name = section_name_updated
        section.section_description = section_description_updated
        # Update the related books
        books_to_update = Books.query.filter_by(sect=sect_name).all()
        for book in books_to_update:
            book.sect = section_name_updated
            
        db.session.commit()
        return jsonify({ "message": "Section Updated"}), 200
        
    return jsonify({"error": "Section not found"}), 404
    
    
#-------------------------------- Delete Section -------------------------------
@app.route("/api/deleteSection/<string:sect_name>", methods = ['DELETE'])
def DeletingSection(sect_name):
    pnd_rtns = Pending_Returns.query.all()
    if pnd_rtns:
        return jsonify({"error": "Deleting a section in this state will rise issues",
               "message": "Please remove all the Pending Returns, before deleting a section."}), 400
        
    section = Section.query.filter_by(section_name=sect_name).first()
    if section:
        # Delete the related books
        books_to_delete = Books.query.filter_by(sect=sect_name).all()
        for book in books_to_delete:
            if removeBook(book.book_id):
                db.session.delete(book)
                
        # Delete the section
        db.session.delete(section)
        db.session.commit()
        cache.delete_memoized(get_user_home_page_data)
        
        return jsonify({ "message": f"Section {sect_name} Deleted Successfully" }), 200
    
    return jsonify({"error": f"{sect_name} doesn't exist in database",
             "message": f"Section {sect_name} is not deleted"}), 400
                 
