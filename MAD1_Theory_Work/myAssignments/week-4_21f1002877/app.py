
import matplotlib.pyplot as plt 
from flask import Flask, render_template, request
app = Flask(__name__)


filename = "data.csv"
file = open(filename,'r')
file.readline() # Read 1st line and Go to 2nd line

data_list = []

for each_line in file:
    list1 = []
    each_line = list(each_line.strip().split(','))  # Separating Values by comma, and then into list

    for word in each_line:  # Converting string to int values.
       list1.append(int(word))  # Single line to single list.

    data_list.append(list1)

file.close()
list1 = []

def html_student(mini_data_list,Total_Marks):
	return render_template("student.html", mini_data_list=mini_data_list, Total_Marks=Total_Marks)
	
def html_wrong():
	return render_template("wrong.html")
	

def html_course(Avg_Marks,Max_Marks):
	return render_template("course.html", Avg_Marks=Avg_Marks, Max_Marks=Max_Marks)
	

@app.route("/", methods=["GET", "POST"])

def main():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        id_type = request.form['ID']
        id_value = request.form['id_value']
        present = False
        
        if ( id_type=="student_id" ):   # If 1st parameter "-s"
        	for each_list in data_list:
        		if str(each_list[0])==id_value : # If student_id  exist in data, then  extract lists of that Student_id.
        			present = True
        			mini_data_list=[]
        			Total_Marks=0
        			for each_list1 in data_list:
        				if each_list1[0]==int(id_value):
        					Total_Marks+=each_list1[2]
        					mini_data_list.append(each_list1)
        					
        			result = html_student(mini_data_list,Total_Marks)
        			break
        			
        	if present==False:
        		result = html_wrong()
        			
        elif ( id_type=="course_id" ):
        	for each_list in data_list:
        		if str(each_list[1])==id_value : # If Course_id  exist in data,
        			present = True
        			Marks=[]
        			Max_Marks=-1
        			Total_Marks=0
        			count=0
        			for each_list1 in data_list:
        				if each_list1[1]==int(id_value):
        					Marks.append(each_list1[2])
        					Total_Marks+=each_list1[2]
        					count+=1
        					if each_list1[2]>Max_Marks:
        						Max_Marks=each_list1[2]
        						
        			plt.clf()
        			plt.hist(Marks)
        			plt.xlabel('Marks')
        			plt.ylabel('Frequency')
        			plt.savefig('static/histogram.png')
        			
        			result = html_course(Total_Marks/count,Max_Marks)
        			break
        			
        	if present==False:
        		result = html_wrong()
        		
        else:
        	result = html_wrong()
        	
        
        return result

if __name__ == '__main__':
    app.run()
