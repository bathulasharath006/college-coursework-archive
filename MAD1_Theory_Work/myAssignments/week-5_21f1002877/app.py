import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.ext.declarative import declarative_base

#current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3" #+ os.path.join(current_dir, "database.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
#db = SQLAlchemy(app)	#CHANGED


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

@app.route("/",methods=["GET"])
def main():
	students = Student.query.all()
	if len(students)==0:
		return render_template("index.html")
	else:
		return render_template("home.html",students=students)

	
@app.route("/student/create", methods=["GET", "POST"])
def create():
	if request.method == "GET":
		return render_template("create.html")
	if request.method == "POST":
		roll_number = request.form['roll']
		first_name = request.form['f_name']
		last_name = request.form['l_name']
		
		student = Student.query.filter_by(roll_number=roll_number).first()
		if student is not None:
			return render_template("already_exists.html")
		else:
			student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
			db.session.add(student)
			db.session.commit()
			
			student = Student.query.filter_by(roll_number=roll_number).first()
			student_id = student.student_id
			
			selected_courses = request.form.getlist("courses")
			courses = { "course_1":1, "course_2":2, "course_3":3, "course_4":4 }
			for course_name in selected_courses:
				enrollment = Enrollments(estudent_id=student_id ,ecourse_id=courses[course_name])
				db.session.add(enrollment)
				
			db.session.commit()
			
			return redirect(url_for("main"))
			

@app.route("/student/<int:student_id>", methods=["GET", "POST"])
def details(student_id):
	student = Student.query.filter_by(student_id=student_id).first()
	enrollments = Enrollments.query.filter_by(estudent_id=student_id).all()
	courses=[]
	for enrollment in enrollments:
		course = db.session.query(Course).get(enrollment.ecourse_id)
		#course = Course.query.get(enrollment.ecourse_id)
		courses.append(course)
	
	return render_template("details.html",student=student, courses=courses)


			
@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update(student_id):
	if request.method == "GET":
		student = Student.query.filter_by(student_id=student_id).first()
		return render_template("update.html",student=student)		
	if request.method == "POST":
		#roll_number = request.form['roll']
		first_name = request.form['f_name']
		last_name = request.form['l_name']
		
		#student = Student.query.get(student_id)
		student = db.session.get(Student, student_id)
		student.first_name = first_name
		if last_name is not None:
			student.last_name = last_name
		db.session.commit()
		
		selected_courses = request.form.getlist("courses")
		current_enrollments = student.enrollments
		courses = { "course_1":1, "course_2":2, "course_3":3, "course_4":4 }
		
		selected_course_ids = {courses[course_name] for course_name in selected_courses}
		
		for enrollment in current_enrollments:
			if enrollment.ecourse_id not in selected_course_ids:
				# Delete any enrollment that is not in the selected courses
				db.session.delete(enrollment)
				
		for course_name in selected_courses:
			course_id = courses[course_name]
			if course_id not in {enrollment.ecourse_id for enrollment in current_enrollments}:
                # Add new enrollments for selected courses that are not in the current enrollments
				enrollment = Enrollments(estudent_id=student_id, ecourse_id=course_id)
				db.session.add(enrollment)

        # Commit the changes to enrollments
		db.session.commit()
			
		return redirect(url_for("main"))		
		
		
@app.route("/student/<int:student_id>/delete", methods=["GET", "POST"])
def delete(student_id):
	if request.method == "GET":
		Enrollments.query.filter_by(estudent_id=student_id).delete()
		Student.query.filter_by(student_id=student_id).delete()
		db.session.commit()
		return redirect(url_for("main"))

if __name__ == '__main__':
	app.run()
