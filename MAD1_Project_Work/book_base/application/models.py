from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email         = db.Column(db.String, unique=True, nullable=False)
    full_name     = db.Column(db.String, nullable=False)
    number        = db.Column(db.String, nullable=False)
    hashed_key    = db.Column(db.String, nullable=False)
    hashed_passwd = db.Column(db.String, nullable=False)
    
    book_id1      = db.Column(db.String)
    book1_issue_dt= db.Column(db.String)
    book_id2      = db.Column(db.String)
    book2_issue_dt= db.Column(db.String)
    book_id3      = db.Column(db.String)
    book3_issue_dt= db.Column(db.String)
    book_id4      = db.Column(db.String)
    book4_issue_dt= db.Column(db.String)
    book_id5      = db.Column(db.String)
    book5_issue_dt= db.Column(db.String)


    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class Admins(db.Model):
    __tablename__ = 'admins'
    
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email         = db.Column(db.String, unique=True, nullable=False)
    full_name     = db.Column(db.String, nullable=False)
    number        = db.Column(db.String, nullable=False)
    hashed_key    = db.Column(db.String, nullable=False)
    hashed_passwd = db.Column(db.String, nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

        
class Books(db.Model):
	__tablename__ = 'books'
	
	sect          = db.Column(db.String, nullable=False)
	book_id       = db.Column(db.String, primary_key=True)
	book_name     = db.Column(db.String, nullable=False)
	authors       = db.Column(db.String, nullable=False)
	synopsis      = db.Column(db.String(1001))
	pages         = db.Column(db.Integer)
	added_on      = db.Column(db.String, nullable=False)
	rating        = db.Column(db.String)


class Requests(db.Model):
	__tablename__ = 'requests'
	
	email         = db.Column(db.String, primary_key=True)
	book_id       = db.Column(db.String, primary_key=True)


class Transactions(db.Model):
	__tablename__ = 'transactions'
	
	id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email         = db.Column(db.String, nullable=False)
	book_id       = db.Column(db.String, nullable=False)
	action        = db.Column(db.String, nullable=False)
	issue_date    = db.Column(db.String)
	return_date   = db.Column(db.String)


class Pending_Returns(db.Model):
	__tablename__ = 'pending_returns'
	
	email         = db.Column(db.String, primary_key=True)
	book_id       = db.Column(db.String, primary_key=True)
	issue_date    = db.Column(db.String)

