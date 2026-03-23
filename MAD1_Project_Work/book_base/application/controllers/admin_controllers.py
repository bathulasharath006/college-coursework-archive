from flask import request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, login_manager
from datetime import datetime as dt, timedelta, date
from flask import current_app as app
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from collections import Counter
import bcrypt
import os, ast


from application.models import * # Tables
from application.validations import * # Additional Security


# ===============================  ADMIN / LIBRARIAN ROUTES  ======================================

#--------------------------------- Admin Logged in page -------------------------------------------
@app.route('/admin_logged_in')
@login_required
def Admin_Logged_in():
	requests = Requests.query.all()
	return render_template('/admin_templates/admin_home_page.html', requests=requests)


#--------------------------- Admin Go's to Library page route --------------------------------------
@app.route("/admin_library_page")
def admin_goto_lib_page():
	
	page = request.args.get('page', 1, type=int)
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
		
	return render_template('admin_templates/admin_goto_lib.html', books=books, avg_rating=avg_rating)


#------------------- Function to perform search based on selected radio button ------------------
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
#---------------------------------------------------------------------------------------------


#------------------------------------- Search Functionality --------------------------------
@app.route('/adminSearch', methods=['GET'])
def Admin_Search():
    if request.method == 'GET':
        searchKey = request.args.get('searchKey', 'all')
        searchQuery = request.args.get('searchQuery').strip()

        books = search_database(searchKey, searchQuery)
        return render_template('/admin_templates/adm_search_pg.html', books=books)
    else:
        return 'Method Not Allowed'


#----------------------------- Function: Issue Date => Return Date ---------------------------------
def Get_Return_Date(issue_dt_in_txt):
	issue_dt = dt.strptime(issue_dt_in_txt, "%Y-%m-%d")
	rtn_dt = ( issue_dt + timedelta(days=7) ).strftime("%Y-%m-%d")
	return rtn_dt


#--------------------------- Admin views Student Details ------------------------------------------
@app.route("/admin/student_details/<string:email>")
def Admin_View_Student_Details(email):
	user = Users.query.filter_by(email=email).first()

	backpack = []
	if user.book_id1 is not None and user.book_id1 != "" and user.book_id1 != " ":
		backpack.append((user.book_id1, user.book1_issue_dt, Get_Return_Date(user.book1_issue_dt)))

	if user.book_id2 is not None and user.book_id2 != "" and user.book_id2 != " ":
		backpack.append((user.book_id2, user.book2_issue_dt, Get_Return_Date(user.book2_issue_dt)))

	if user.book_id3 is not None and user.book_id3 != "" and user.book_id3 != " ":
		backpack.append((user.book_id3, user.book3_issue_dt, Get_Return_Date(user.book3_issue_dt)))

	if user.book_id4 is not None and user.book_id4 != "" and user.book_id4 != " ":
		backpack.append((user.book_id4, user.book4_issue_dt, Get_Return_Date(user.book4_issue_dt)))

	if user.book_id5 is not None and user.book_id5 != "" and user.book_id5 != " ":
		backpack.append((user.book_id5, user.book5_issue_dt, Get_Return_Date(user.book5_issue_dt)))
	
	return render_template('admin_templates/student_details.html', user=user, backpack=backpack )


#--------------------------- Admin views Book Details -----------------------------
@app.route("/admin/book_details/<string:book_id>")
def Admin_View_Book_Details(book_id):
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

	return render_template('admin_templates/admin_book_details.html', book=book, avg_rating=avg_rating )


#--------------------------- Admin Accepts Book Request ----------------------------
@app.route("/admin/accept_request/<string:email>/<string:book_id>" )
def Accept_Request(email, book_id):
	request = Requests.query.filter_by(email=email, book_id=book_id).first()
	db.session.delete(request) # Remove from Requests Table
	
	issue_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction = Transactions( email=email, book_id=book_id, action="Accept", issue_date=issue_date )
	db.session.add(transaction)  # Add Transaction into dataBase
	
	pend_rtns = Pending_Returns(email=email, book_id=book_id, issue_date=issue_date)
	db.session.add(pend_rtns) # Add Book into Pending Returns

	issue_dt = dt.now().strftime("%Y-%m-%d")	
	user = Users.query.filter_by(email=email).first() # Add Book into Users Table
	if user.book_id1 is None or user.book_id1 == "" or user.book_id1 == " ":
		user.book_id1  = book_id
		user.book1_issue_dt = issue_dt
	elif user.book_id2 is None or user.book_id2 == "" or user.book_id2 == " ":
		user.book_id2 = book_id
		user.book2_issue_dt = issue_dt
	elif user.book_id3 is None or user.book_id3 == "" or user.book_id3 == " ":
		user.book_id3 = book_id
		user.book3_issue_dt = issue_dt
	elif user.book_id4 is None or user.book_id4 == "" or user.book_id4 == " ":
		user.book_id4 = book_id
		user.book4_issue_dt = issue_dt
	elif user.book_id5 is None or user.book_id5 == "" or user.book_id5 == " ":
		user.book_id5 = book_id
		user.book5_issue_dt = issue_dt
	
	db.session.commit()
	return redirect(url_for('Admin_Logged_in'))


#--------------------------- Admin Rejects Book Request ----------------------
@app.route("/admin/reject_request/<string:email>/<string:book_id>" )
def Reject_Request(email, book_id):

	issue_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction = Transactions( email=email, book_id=book_id, action="Reject", issue_date=issue_date )
	db.session.add(transaction)  # Add Transaction into dataBase
	
	request = Requests.query.filter_by(email=email, book_id=book_id).first()
	db.session.delete(request) # Remove from Requests Table
	db.session.commit()
	return redirect(url_for('Admin_Logged_in'))


#--------------------------- Admin checks Pending Returns ----------------------
@app.route("/admin/pending_returns" )
def Pending_Books_List():
	rows = Pending_Returns.query.all()
	pnd_rtns = []
	for each in rows:
		pnd_rtns.append( (each.email, each.book_id, each.issue_date , Get_Return_Date(each.issue_date.split()[0])) )
	
	return render_template('admin_templates/admin_pnding_returns.html', pnd_rtns=pnd_rtns )


#--------------------------- Admin Revoke's Book Access ----------------------
@app.route("/admin/revoke/<string:email>/<string:book_id>/<string:page>" )
def Revoke_Book_Access( email, book_id, page):

	user = Users.query.filter_by(email=email).first()
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

	pend_rtn = Pending_Returns.query.filter_by( email=email, book_id=book_id).first()
	transaction = Transactions.query.filter_by( email=email, book_id=book_id, issue_date=pend_rtn.issue_date ).first()
	return_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	transaction.return_date = return_date # Add Return date to Transactions
	
	db.session.delete(pend_rtn) # Remove from Pending Returns
	db.session.commit()
	
	if page == 'pndig_returns':
		return redirect(url_for('Pending_Books_List'))
	elif page == 'stdn_dtls':
		return redirect( url_for( 'Admin_View_Student_Details', email=email))


# ================================ STATISTICS ROUTES  ======================================


basedir = os.path.abspath(os.path.dirname(__file__))
PLOTS_DIR = os.path.join(basedir, "../../static/plots/")
#------------------------------ Charts Home Page ---------------------------------------
@app.route("/statistics")
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
	plt.clf()
	
	#---- Top 10 Books Borrowers ----#
	emails = [ tran.email for tran in trans]	
	emails_dict = Counter(emails)
	emails = dict(sorted(emails_dict.items(), key=lambda item: item[1]))
	
	first_10_emails = dict(list(emails.items())[:10])
	
	emails = list(first_10_emails.keys())
	x = [ user_mail.strip('@gmail.com') for user_mail in emails ]
	y = list(first_10_emails.values())
	cmap = plt.cm.get_cmap('gist_rainbow')
	max_value = max(y)
	normalized_values = [each_y / max_value for each_y in y]
	
	plt.figure(figsize=(9, 6))
	bars = plt.bar(x, y, width= 0.2, color=cmap(normalized_values))
	plt.bar_label(bars )
	plt.savefig(PLOTS_DIR + 'popular_borrowers.png', bbox_inches='tight')
	plt.clf()

	#---- 30 Days Scatter Plot ----#
	transactions = Transactions.query.all()
	data = [{"id": tran.id, "action": tran.action, "issue_date": date( int(tran.issue_date[:4]),
		  int(tran.issue_date[5:7].lstrip('0')), int(tran.issue_date[8:10].lstrip('0')) )} for tran in transactions]

	df = pd.DataFrame(data)

	# Filter data for the past 10 days
	end_date = dt.now().date()
	start_date = end_date - timedelta(days=9)
	filtered_df = df[(df['issue_date'] >= start_date) & (df['issue_date'] <= end_date)]

	# Separate data for "Accept" and "Reject" actions
	accept_data = filtered_df[filtered_df['action'] == 'Accept']
	reject_data = filtered_df[filtered_df['action'] == 'Reject']
	agg_data = filtered_df.groupby(['issue_date', 'action']).size().unstack(fill_value=0)

	plt.figure(figsize=(22, 5))	
	plt.scatter(agg_data.index, agg_data['Accept'], color='green', label='Accept') # Plot accepts
	for i, count in enumerate(agg_data['Accept']):
		plt.annotate(str(count), (agg_data.index[i], count), textcoords="offset points", xytext=(10,10), ha='center')

	plt.scatter(agg_data.index, agg_data['Reject'], color='red', label='Reject') # Plot rejects
	for i, count in enumerate(agg_data['Reject']):
		plt.annotate(str(count), (agg_data.index[i], count), textcoords="offset points", xytext=(-10,-10), ha='center')

	plt.plot(agg_data.index, agg_data['Accept'], color='green', linestyle='-', linewidth=1)
	plt.plot(agg_data.index, agg_data['Reject'], color='red', linestyle='-', linewidth=1)

	plt.legend()
	plt.xticks(rotation=45)
	plt.grid(True)
	plt.savefig(PLOTS_DIR + 'scatter.png', bbox_inches='tight')
	plt.clf()

	return render_template('admin_templates/Statistics/statistics.html')


#--------------------------------- BookWise Statistics ------------------------------------
@app.route("/bookStats")
def Book_Statistics():

	book_id = request.args.get('GetDetails', '').strip().upper()
	book = Books.query.filter_by(book_id=book_id).first()
	
	if book is None:
		return render_template('admin_templates/Statistics/book_stat.html', book_id=None)			
	else:
		# Pie Chart for Accept vs Reject
		accept_count = Transactions.query.filter_by(book_id=book_id, action='Accept').count()
		reject_count = Transactions.query.filter_by(book_id=book_id, action='Reject').count()

		counts = [accept_count, reject_count]
		labels = ['Accept', 'Reject']
		colors = ['#08df12', '#f51009']

		plt.figure(figsize=(5, 5))
		plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors)
		plt.axis('equal')
		
		plt.text(1, 1, f'Accept: {accept_count}\nReject: {reject_count}', horizontalalignment='right', verticalalignment='top')
		plt.savefig(PLOTS_DIR + 'Accept_Vs_Reject.png', bbox_inches='tight')
		plt.clf()

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
		plt.clf()
		
		return render_template('admin_templates/Statistics/book_stat.html', book_id=book_id)			


#--------------------------------- Section Statistics ------------------------------------
@app.route("/sectionStats")
def Section_Statistics():
	
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
	plt.clf()
		
	return render_template('admin_templates/Statistics/sect_stat.html',)			


#-------------------------------- Transactions Page ---------------------------------------
@app.route("/transactions")
def TransactionsPage():

	page = request.args.get('page', 1, type=int)
	trans = Transactions.query.order_by(Transactions.id.desc()).paginate(page=page, per_page=17)
	return render_template('admin_templates/Statistics/transactions.html', trans=trans)


# =============================== ACCOUNT CRUD ROUTES  ======================================

#------------------------- New Librarian Registration ---------------------------------------
@app.route("/registerLibrarian", methods = ['POST'])
def registering_admin():
    if request.method == 'POST':
        email = request.form['email'].strip()
        full_name = request.form['full_name'].strip().upper()
        number = request.form['number'].strip()
        create_password = request.form['create_password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        key = request.form['key'].strip()
        
        admin = Admins.query.filter_by(email=email).first()
        if admin :
            error = "An account with this email already exists.<br> Log in or try registering with another email."
            return render_template( "admin_templates/adm_registeration.html",  error=error)
                        
        else:
            error = valid_register(email, full_name, number, create_password, confirm_password, key)
            if error :
                return render_template('registration.html',error=error)
            
            hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
            admin = Admins(email=email, full_name=full_name, number=number, hashed_key=hashed_key, hashed_passwd=hashed_passwd)
            db.session.add(admin)
            db.session.commit()
            
            heading = "Registration Success!"
            message = "With Great Power, Comes Great Responsibility."
            ending = "Congratulations"
            url = '/admin_logged_in'
            return render_template('success.html', heading=heading, message=message, ending=ending, url=url)


#---------------------------- Get Librarian Details & Update Account Info  => Home page ----------------
@app.route("/update_librarian_details",  methods = ['GET', 'POST'])
def Updating_librarian_details():

	if request.method == 'GET':
		email = request.args.get('GetDetails', '').strip()
		admin = Admins.query.filter_by(email=email).first()
		if admin is None:
			noDetailsMessage = 'No details found for the given email'
			return render_template('update_details.html', role="Librarian", email=email, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('update_details.html', role="Librarian",\
		            email=admin.email, full_name=admin.full_name, number=admin.number)

	elif request.method == 'POST':
		email = request.form['email'].strip()
		full_name = request.form['full_name'].strip().upper()
		number = request.form['number'].strip()
		create_password = request.form['create_password'].strip()
		confirm_password = request.form['confirm_password'].strip()
		key = request.form['key'].strip()
		
		admin = Admins.query.filter_by(email=email).first()
		if admin :
			error=''
			error = valid_register(email, full_name, number, create_password, confirm_password, key)
			if error :
				return render_template('update_details.html', role="Librarian", email=email, noDetailsMessage=error)
			
			hashed_key, hashed_passwd = key_paswd_bcrypt(key, create_password)
			admin.full_name = full_name
			admin.number = number
			admin.hashed_key = hashed_key
			admin.hashed_passwd = hashed_passwd
			db.session.commit()

			heading = "Account Details Updated!"
			message = "Power cannot simply be enjoyed for its privileges alone but necessarily makes its holders morally responsible."
			ending = "Successfully"
			url = '/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
		else:
			return redirect(url_for('Admin_Logged_in'))


#---------------------------- Get Librarian Details & Delete Account =>Home page ----------------
@app.route("/delete_librarian_account",  methods = ['GET', 'POST'])
def deleting_librarian_account():

	if request.method == 'GET':
		role = "Librarian"
		email = request.args.get('GetDetails', '').strip()
		admin = Admins.query.filter_by(email=email).first()
		if admin is None:
			noDetailsMessage = 'No details found for the given email'
			return render_template('delete_account.html', role=role, email=email, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('delete_account.html', role=role, email=admin.email, full_name=admin.full_name, number=admin.number)
	    
	elif request.method == 'POST':
		email = request.form['email'].strip()
		
		admin = Admins.query.filter_by(email=email).first()
		if admin :
			db.session.delete(admin)
			db.session.commit()

			heading = "Account Deleted!"
			message = "Sorry to see you Go!	 Come Back Soon.... 	Nothing is pleasanter than exploring a library."
			ending = "Successfully"
			url = '/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
		else:
			return redirect(url_for('Admin_Logged_in'))


# ===============================  BOOKS CRUD ROUTES  ======================================

#---------------------------------- Add New Book -------------------------------------------
@app.route("/admin_add_book", methods=['POST'])
def admin_adding_book():
	if request.method =='POST':
		sect      = request.form['sect'].strip().upper()
		book_id   = request.form['book_id'].strip().upper()
		book_name = request.form['book_name'].strip()
		authors   = request.form['authors'].strip().upper()
		synopsis  = request.form['synopsis'].strip()
		pages     = request.form['pages'].strip()
		cover_pg  = request.files['image']
		pdf_file  = request.files['pdfFile']
		added_on  = dt.now().strftime("%Y-%m-%d")

		book = Books.query.filter_by(book_id=book_id).first()		
		if book :
			return render_template('books_templates/book_already_exist.html', book=book )
		else:
			error = valid_addBook(sect, book_id, book_name, authors, synopsis, cover_pg, pdf_file, added_on )
			if error :
				return render_template('books_templates/add_book.html',error=error)
			
			# Rename files based on book ID
			image_filename = f'{book_id}.jpg'
			pdf_filename = f'{book_id}.pdf'
			
			# Save the files to the specified upload folder
			cover_pg.save(app.config['UPLOAD_FOLDER'] + '/' + image_filename)
			pdf_file.save(app.config['UPLOAD_FOLDER'] + '/' + pdf_filename)
			
			rating = '{ 1:0, 2:0, 3:0, 4:0, 5:0 }'
			book = Books( sect=sect, book_id=book_id, book_name=book_name, authors=authors,
			           synopsis=synopsis, pages=pages, added_on=added_on, rating = rating)
			db.session.add(book)
			db.session.commit()

			heading = "Book Added!"
			message = "Books are important for the mind, heart, and soul."
			ending = "More Books, More Knowledge"
			url = '/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)


#----------------------------- Update Book ------------------------------------------------
@app.route("/admin_update_book",  methods = ['GET', 'POST'])
def admin_updates_book():

	if request.method == 'GET':
		book_id = request.args.get('GetDetails', '').strip().upper()
		book = Books.query.filter_by(book_id=book_id).first()
		if book is None:
			noDetailsMessage = 'No details found for the given book id'
			return render_template('books_templates/update_book.html', book_id=book_id, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('books_templates/update_book.html', sect=book.sect.title(), book_id=book.book_id,
		            book_name=book.book_name.title(), authors=book.authors.title(), synopsis=book.synopsis, pages=book.pages, added_on=book.added_on )

	elif request.method == 'POST':
		sect      = request.form['sect'].strip().upper()
		book_id   = request.form['book_id'].strip().upper()
		book_name = request.form['book_name'].strip().upper()
		authors   = request.form['authors'].strip().upper()
		synopsis  = request.form['synopsis'].strip()
		pages = request.form['pages'].strip()
		
		book = Books.query.filter_by(book_id=book_id).first()
		if book :	
			book.sect = sect
			book.book_name = book_name
			book.authors = authors
			book.synopsis = synopsis
			book.pages = pages
			db.session.commit()

			heading = "Book Updated!"
			message = "There is more treasure in books than in all the pirate's loot on Treasure Island."
			ending = "Walt Disney"
			url = '/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
		else:
			return redirect(url_for('Admin_Logged_in'))


#----------------------------- Delete Book  -----------------------------------------------
@app.route("/admin_delete_book",  methods = ['GET', 'POST'])
def admin_deletes_book():

	if request.method == 'GET':
		book_id = request.args.get('GetDetails', '').strip().upper()
		book = Books.query.filter_by(book_id=book_id).first()
		if book is None:
			noDetailsMessage = 'No details found for the given book id'
			return render_template('books_templates/delete_book.html', book_id=book_id, noDetailsMessage=noDetailsMessage)
		else:
		    return render_template('books_templates/delete_book.html', sect=book.sect, book_id=book.book_id,
		            book_name=book.book_name, authors=book.authors, synopsis=book.synopsis, pages=book.pages, added_on=book.added_on )

	elif request.method == 'POST':
		book_id = request.form['book_id'].strip()
		
		book = Books.query.filter_by(book_id=book_id).first()
		if book :
		
			image_filename = f'{book_id}.jpg'
			pdf_filename = f'{book_id}.pdf'
		
			image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
			pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

			os.remove(image_path)
			os.remove(pdf_path)
				
			db.session.delete(book)
			db.session.commit()

			heading = "Book Deleted!"
			message = "Reading is essential for those who seek above the ordinary."
			ending = "Jim Rohn"
			url = '/admin_logged_in'
			return render_template('success.html', heading=heading, message=message, ending=ending, url=url)
			
		else:
			return redirect(url_for('Admin_Logged_in'))


