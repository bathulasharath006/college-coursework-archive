import sys
from jinja2 import Template
import matplotlib.pyplot as plt


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



TEMPLATE1 ="""
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title>Student Data</title>
</head>
<body>
     <h1>Student Details</h1>
    <table border=1>
        <thead>
            <tr>
              <th>Student id</th>
              <th>Course id</th>
              <th>Marks</th>
          </tr>
        </thead>
        <tbody>
            {% for each_list in mini_data_list %}
            <tr>
                <td>{{ each_list[0] }}</td>
                <td>{{ each_list[1] }}</td>
                <td>{{ each_list[2] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan=2 style="text-align: center;" >Total Marks</td>
                <td>{{ Total_Marks }}</td>
            </tr>
        </tbody>
    </table>                    
</body>
</html>
"""


TEMPLATE2 ="""
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title>Course Data</title>
</head>
<body>
     <h1>Course Details</h1>
    <table border=1>
        <thead>
            <tr>
              <th>Average Marks</th>
              <th>Maximum Marks</th>
          </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ Avg_Marks }}</td>
                <td>{{ Max_Marks }}</td>
            </tr>
        </tbody>
    </table>                    
            <img src='histogram.png'>
</body>
</html>
"""


TEMPLATE3 ="""
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title>Something Went Wrong</title>
</head>
<body>
     <h1>Wrong Inputs</h1>
     <p>Something went wrong</P>
</body>
</html>
"""


def html_wrong():
	template = Template(TEMPLATE3)
	my_html_document_file = open('output.html', 'w')
	my_html_document_file.write(template.render())
	my_html_document_file.close()


def html_student(mini_data_list,Total_Marks):
	template = Template(TEMPLATE1)
	my_html_document_file = open('output.html', 'w')
	my_html_document_file.write(template.render(mini_data_list=mini_data_list,Total_Marks=Total_Marks))
	my_html_document_file.close()


if ( sys.argv[1]=="-s" ):   # If 1st parameter "-s"
    for each_list in data_list:
        if str(each_list[0])==sys.argv[2] : # If student_id  exist in data, then  extract lists of that Student_id.

            mini_data_list=[]
            Total_Marks=0
            for each_list1 in data_list:
                if each_list1[0]==int(sys.argv[2]):
                    Total_Marks+=each_list1[2]
                    mini_data_list.append(each_list1)

            html_student(mini_data_list,Total_Marks)
            exit()

    html_wrong()
    exit()



def html_course(Avg_Marks,Max_Marks):
	template = Template(TEMPLATE2)
	my_html_document_file = open('output.html', 'w')
	my_html_document_file.write(template.render(Avg_Marks=Avg_Marks,Max_Marks=Max_Marks))
	my_html_document_file.close()


if ( sys.argv[1]=="-c" ):   # If 1st parameter "-c"
    for each_list in data_list:
        if str(each_list[1])==sys.argv[2] : # If Course_id  exist in data,


            Marks=[]
            Max_Marks=-1
            Total_Marks=0
            count=0
            for each_list1 in data_list:
                if each_list1[1]==int(sys.argv[2]):
                    Marks.append(each_list1[2])
                    Total_Marks+=each_list1[2]
                    count+=1
                    if each_list1[2]>Max_Marks:
                        Max_Marks=each_list1[2]

            plt.hist(Marks)
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.savefig('histogram.png')

            html_course(Total_Marks/count,Max_Marks)
            exit()

    html_wrong()
    exit()

html_wrong()
