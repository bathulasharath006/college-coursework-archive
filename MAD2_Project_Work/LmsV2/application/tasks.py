from application.workers import celery
from application.models import *
from datetime import datetime as dt, timedelta
from application.mail_service import send_email
from collections import defaultdict
from jinja2 import Template
import os, weasyprint


#--------------------- Function: Issue Date => Return Date ---------------------
def Get_Return_Date(issue_dt_in_txt):
	issue_dt = dt.strptime(issue_dt_in_txt, "%Y-%m-%d")
	rtn_dt = ( issue_dt + timedelta(days=7) ).strftime("%Y-%m-%d")
	return rtn_dt
	
#-------------------------- After 7 Days Remove Access -------------------------
@celery.task
def Auto_Access_Revoke():
	pd_rtns = Pending_Returns.query.all()
	current_date = dt.now().strftime("%Y-%m-%d")
	for each in pd_rtns:
	    return_date = Get_Return_Date( each.issue_date.split()[0] )
	    if current_date > return_date:
	        # Remove Book from User
	        user = Users.query.filter_by(email=each.email).first()
	        books_borrowed = eval(user.books_borrowed)
	        if each.book_id in books_borrowed:
	            del books_borrowed[each.book_id]
	            user.books_borrowed = str(books_borrowed)
	            
	        # Add Return date to Transactions & Update transactions
	        transaction = Transactions.query.filter_by( email=each.email,
	                 book_id=each.book_id, issue_date=each.issue_date ).first()
	        return_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")
	        transaction.return_date = return_date
	        
	        # Remove from Pending Returns
	        db.session.delete(each)
	        db.session.commit() # Commit for each user.
	print("Auto Access Revoke Function call is Completed.")


# ------------------- Check User Activity & Book Return Dates --------------------
@celery.task
def Daily_Reminders():
    current_date = dt.now().strftime("%Y-%m-%d")
    tomorrow_date = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Fetch all users
    users = Users.query.all()
    
    for user in users:
        # Check if user has not visited today
        if user.last_login.split()[0] != current_date:
            send_email(
                to_address=user.email,
                subject="Reminder: You have not visited your account today",
                message=f"Hello {user.full_name},<br><br>You have not visited your account today. Please login to stay updated." )
        
        # Check if any borrowed book has a return date of tomorrow
        if user.books_borrowed:
            books_borrowed = eval(user.books_borrowed)
            for book_id, issue_date in books_borrowed.items():
                return_date = Get_Return_Date( issue_date )
                if return_date == tomorrow_date:
                    send_email(
                        to_address=user.email,
                        subject="Reminder: Book Return Due Tomorrow",
                        message=f"Hello {user.full_name},<br><br>Your borrowed book (ID: {book_id}) is due for return tomorrow ({return_date}). Please make sure to return it on time."
                    )
    
    print("Daily Reminders task completed.")


# ------------------------------ Monthly Report --------------------------------    
# ---------------------- Function: Returns Summary Data ------------------------
def process_summary_data():
    sects = Section.query.all()
    books_in_sections = []
    for row in sects:  # No. of books in each section in the library
        books_in_sections.append({
            'sect_name': row.section_name,
            'count': len(eval(row.books_ids)) })

    total_books_count = Books.query.count()  # Total No. of books in the library
    no_of_users = Users.query.filter_by(access_level=1).count()  # Total users in the library

    today = dt.today()
    if today.month == 1:
        last_month_pattern = f"{today.year - 1}-12-%"
    else:
        last_month_pattern = f"{today.year}-{today.month - 1:02d}-%"

    transactions = Transactions.query.filter(
        Transactions.issue_date.like(last_month_pattern)).all()

    transactions_count = len(transactions)  # No. of txns in the last month
    accepted_count = 0  # Accept count in the last month
    rejected_count = 0  # Reject count in the last month
    book_request_count = defaultdict(int)  # Each book request count in the last month
    user_request_count = defaultdict(int)  # Each user request count in the last month
    transactions_by_date = defaultdict(lambda: {"Accept": 0, "Reject": 0})

    for txn in transactions:
        txn_date = txn.issue_date.split(" ")[0]
        book_request_count[txn.book_id] += 1
        user_request_count[txn.email] += 1

        if txn.action == 'Accept':
            accepted_count += 1
            transactions_by_date[txn_date]["Accept"] += 1
        elif txn.action == 'Reject':
            rejected_count += 1
            transactions_by_date[txn_date]["Reject"] += 1

    return {
        "books_in_sections": books_in_sections,
        "total_books_count": total_books_count,
        "no_of_users": no_of_users,
        "transactions_count": transactions_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "book_request_count": dict(book_request_count),
        "user_request_count": dict(user_request_count),
        "transactions_by_date": dict(transactions_by_date) }

# ---------------- Function: summary_data => Return html report ----------------
def generate_html_report(data):
    template = Template("""
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
            }
            h1, h2, h3 {
                color: #333;
            }
            table {
                margin: 0 auto; /* Center the table */
                border-collapse: collapse;
                width: 80%;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            p {
                text-align: left; /* Left-align the paragraphs within the centered content */
                margin-left: 10%;
                margin-right: 10%;
            }
        </style>
    </head>
    <body>
        <h1>Monthly Library Report - {{ report_date }}</h1>
        
        <h2>Library Summary</h2>
        <p>Total Books: {{ total_books_count }}</p>
        <p>Total Users: {{ no_of_users }}</p>
        
        <h2>Books in Each Section</h2>
        <table border="1">
            <tr>
                <th>Section</th>
                <th>Number of Books</th>
            </tr>
            {% for section in books_in_sections %}
            <tr>
                <td>{{ section.sect_name }}</td>
                <td>{{ section.count }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <h2>Transactions Summary</h2>
        <p>Total Transactions: {{ transactions_count }}</p>
        <p>Accepted: {{ accepted_count }}</p>
        <p>Rejected: {{ rejected_count }}</p>
        
        <h3>Transactions by Date</h3>
        <table border="1">
            <tr>
                <th>Date</th>
                <th>Accepted</th>
                <th>Rejected</th>
            </tr>
            {% for date, counts in transactions_by_date.items() %}
            <tr>
                <td>{{ date }}</td>
                <td>{{ counts.Accept }}</td>
                <td>{{ counts.Reject }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <h3>Book Requests</h3>
        <table border="1">
            <tr>
                <th>Book ID</th>
                <th>Request Count</th>
            </tr>
            {% for book_id, count in book_request_count.items() %}
            <tr>
                <td>{{ book_id }}</td>
                <td>{{ count }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <h3>User Requests</h3>
        <table border="1">
            <tr>
                <th>User Email</th>
                <th>Request Count</th>
            </tr>
            {% for email, count in user_request_count.items() %}
            <tr>
                <td>{{ email }}</td>
                <td>{{ count }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """)
    return template.render(report_date=dt.today().strftime("%Y-%m-%d"), **data )

@celery.task
def Send_Monthly_Report():
    report_data = process_summary_data() # Process data
    html_report = generate_html_report(report_data) # Generate HTML report
    
    # Generate PDF report
    pdf_path = os.path.join(
          os.path.abspath(os.path.dirname(__file__)),
          "../db_directory/Monthly_Reports/",
          f"Monthly_Report_{dt.today().strftime('%Y_%m_%d')}.pdf" )
          
    weasyprint.HTML(string=html_report).write_pdf(pdf_path)
    
    users = Users.query.filter_by(access_level=0).all()
    for user in users:
        send_email( to_address = user.email,
             subject = f"Monthly Library Report - {dt.today().strftime('%B %Y')}",
             message = html_report )

    print("Monthly Report sent to all Librarians.")
# ------------------------------------------------------------------------------

# ----------------------------- Export CSV Report ------------------------------
@celery.task
def export_csv():
    transactions = Transactions.query.all()
    
    csv_path = os.path.join(
          os.path.abspath(os.path.dirname(__file__)),
          "../frontend/public/transactions.csv")
        
    with open(csv_path, 'w') as csvfile:
        csvfile.write("#, Email, Book ID, Action, Date Issued, Return Date\n")
        for txn in transactions:
            csvfile.write(f"{txn.id}, {txn.email}, {txn.book_id}, {txn.action}, {txn.issue_date}, {txn.return_date}\n")
    
    return "static/transactions.csv"
