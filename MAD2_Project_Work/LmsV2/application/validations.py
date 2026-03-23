import bcrypt

#-------------------- Plain key and Password into Hash Passwords ----------------------------- 
def key_paswd_bcrypt(key, create_password):
    salt = bcrypt.gensalt()
    hashed_key = bcrypt.hashpw(key.encode('utf-8'), salt)
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(create_password.encode('utf-8'), salt)
    
    return hashed_key, hashed_passwd


#----------------------------------- Password Check ------------------------------------------
def check_password_bcrypt(password, hashed_passwd):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_passwd)


# Backend Validations

#--------------------Validating entries before Proceeding Further ----------------------------
def valid_register(email, full_name, number, create_password, confirm_password, key):
    error = ''
    if '@' and '.' not in email:
        error += "Enter a proper Mail address.<br>"
    if full_name == '':
        error += "Name can not be Empty.<br>"
    if len(number) != 10 or not number.isnumeric():
        error += "Mobile Number is in wrong format.<br>"
    if len(create_password) < 8:
        error += "Password must be atleast 8 characters long."
    if create_password != confirm_password:
        error += "Passwords are not matching"
    if len(key) != 6 or not key.isnumeric():
        error += "Secret Key must be 6 digits.<br>"
    
    return error



#	FOR BOOKS
# -------------------Allowed file extensions for images and PDFs--------------------------------
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
#----------------------------------------------------------------------------------------------



#--------------------Validating entries before Proceeding Further ----------------------------
def valid_addBook(sect, book_id, book_name, authors, synopsis, cover_pg, pdf_file, added_on ):
	error = ''
	if   sect == '' or book_id == '' or book_name == '' or authors == '' or len(synopsis) > 1002 or \
	             added_on == '' or pdf_file.filename == '' or cover_pg.filename=='' :
	     
		error += "Necessary fields can not be empty and invalid data format is supplied.<br>"
	
	if ( not allowed_file(cover_pg.filename, ALLOWED_IMAGE_EXTENSIONS) or \
	not allowed_file(pdf_file.filename, ALLOWED_PDF_EXTENSIONS) ):
		error += "Invalid file format.<br>Allowed formats: images (png, jpg, jpeg) and PDFs"
	return error


