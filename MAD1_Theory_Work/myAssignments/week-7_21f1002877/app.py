
#-----------------------------Imports-------------------------------------
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_

#-----------------------------Configurations-------------------------------------
current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "week7_database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


#-----------------------------Models-------------------------------------
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer,   db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer,  db.ForeignKey("course.course_id"), nullable=False)
    
Student.enrollments = db.relationship("Enrollments", backref="student")
Course.enrollments = db.relationship("Enrollments", backref="course")


#-----------------------------Routes------------------------------------


#----------------------------Home Pages of Students----------------------
@app.route("/",methods=["GET"])
def main():
	students = Student.query.all()
	if len(students)==0:
		return render_template("index_students.html")
	else:
		return render_template("home_students.html",students=students)
		

#-------------------------  + Add Student Pages  ---------------------------
@app.route("/student/create", methods=["GET", "POST"])
def create_student():
	if request.method == "GET":
		return render_template("create_student.html")
	if request.method == "POST":
		roll_number = request.form['roll']
		first_name = request.form['f_name']
		last_name = request.form['l_name']
		
		student = Student.query.filter_by(roll_number=roll_number).first()
		if student is not None:
			return render_template("student_already_exists.html")
		else:
			student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
			db.session.add(student)
			db.session.commit()
			return redirect(url_for("main"))


#----------------------Update Student Pages--------------------------			
@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
	if request.method == "GET":
		student = Student.query.filter_by(student_id=student_id).first()
		enrolled_course_ids = [enrollment.ecourse_id for enrollment in db.session.get(Student, student_id).enrollments]
		courses_not_enrolled = Course.query.filter(not_(Course.course_id.in_(enrolled_course_ids))).all()

		return render_template("update_student.html",student=student, courses=courses_not_enrolled)
		
	if request.method == "POST":
		#roll_number = request.form['roll']
		first_name = request.form['f_name']
		last_name = request.form['l_name']
		course_id = request.form.get("course", None)
		#course_id = request.form["course"] This line is throwing an error.
		
		#student = Student.query.get(student_id)
		student = db.session.get(Student, student_id)
		student.first_name = first_name
		if last_name is not None:
			student.last_name = last_name
		db.session.commit()
		
		if course_id is not None:
			new_enrollment = Enrollments(estudent_id=student_id, ecourse_id=course_id)
			db.session.add(new_enrollment)
			db.session.commit()
			
		return redirect(url_for("main"))


#------------------Student and Enrollments delete function------------------	
@app.route( "/student/<int:student_id>/delete" )
def delete_student(student_id):
	if request.method == "GET":
		Enrollments.query.filter_by(estudent_id=student_id).delete()
		Student.query.filter_by(student_id=student_id).delete()
		db.session.commit()
		return redirect(url_for("main"))


#----------------------Student Details----------------------------
@app.route( "/student/<int:student_id>" )
def student_details(student_id):
	student = Student.query.filter_by(student_id=student_id).first()
	enrollments = Enrollments.query.filter_by(estudent_id=student_id).all()
	courses=[]
	for enrollment in enrollments:
		course = db.session.get(Course, enrollment.ecourse_id)
		#course = Course.query.get(enrollment.ecourse_id)
		courses.append(course)
	
	return render_template("student_details.html",student=student, courses=courses)


#----------------------Student: Course WithDraw function----------------------------
@app.route( "/student/<int:student_id>/withdraw/<int:course_id>" )
def with_draw(student_id, course_id ):
	Enrollments.query.filter_by(estudent_id=student_id, ecourse_id=course_id).delete()
	db.session.commit()
	return redirect(url_for("main"))



#----------------------------Home Pages of Courses----------------------
@app.route("/courses", methods=["GET", "POST"])
def course():
	courses = Course.query.all()
	if len(courses)==0:
		return render_template("index_courses.html")
	else:
		return render_template("home_courses.html",courses=courses)

			
#-------------------------  + Add Course Pages  ---------------------------
@app.route("/course/create", methods=["GET", "POST"])
def create_course():
	if request.method == "GET":
		return render_template("create_course.html")
	if request.method == "POST":
		course_code = request.form['code']
		course_name = request.form['c_name']
		course_description = request.form['desc']
		
		course = Course.query.filter_by(course_code=course_code).first()
		if course is not None:
			return render_template("course_already_exists.html")
		else:
			course = Course(course_code=course_code, course_name=course_name, course_description=course_description)
			db.session.add(course)
			db.session.commit()
			return redirect(url_for("course"))


#----------------------Update Course Pages--------------------------			
@app.route("/course/<int:course_id>/update", methods=["GET", "POST"])
def update_course(course_id):
	if request.method == "GET":
		course = Course.query.filter_by(course_id=course_id).first()
		
		return render_template( "update_course.html",course=course )
		
	if request.method == "POST":
		#course_code = request.form['code']
		course_name = request.form['c_name']
		course_description = request.form['desc']
		
		course = db.session.get(Course, course_id)
		course.course_name = course_name
		if course_description is not None:
			course.course_description = course_description
		db.session.commit()
			
		return redirect(url_for("course"))


#------------------Course and Enrollments delete function------------------	
@app.route( "/course/<int:course_id>/delete" )
def delete_course(course_id):
	if request.method == "GET":
		Enrollments.query.filter_by(ecourse_id=course_id).delete()
		Course.query.filter_by(course_id=course_id).delete()
		db.session.commit()
		return redirect(url_for("main"))


#----------------------Course Details----------------------------
@app.route( "/course/<int:course_id>" )
def course_details(course_id):
	course = Course.query.filter_by(course_id=course_id).first()
	enrollments = Enrollments.query.filter_by(ecourse_id=course_id).all()
	students=[]
	for enrollment in enrollments:
		student= db.session.get(Student, enrollment.estudent_id)
		students.append(student)
	
	return render_template("course_details.html", course=course, students=students )

	

if __name__ == '__main__':
	debug = True
	app.run()
