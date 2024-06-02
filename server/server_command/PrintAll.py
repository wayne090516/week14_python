import json
from table.StudentInfoTable import StudentInfoTable
from table.ParametersTable import ParametersTable

class PrintAll:
    def __init__(self, connection, parameters):
        self.connection = connection

    def execute(self):
        student_dict = {}
        StudentInfo = StudentInfoTable()
        Parameters = ParametersTable()

        student_names_dict = StudentInfo.select_all_students()
        
        for name, stu_id in student_names_dict.items():
            student_dict[name] = Parameters.select_a_subject(stu_id)          

        response = {'status': 'OK', 'parameters': student_dict}
        #json_str = json.dumps(response)
        #print("JSON string:", json_str)                   
        self.connection.send(json.dumps(response).encode())
