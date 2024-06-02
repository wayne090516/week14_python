from table.StudentInfoTable import StudentInfoTable
from table.ParametersTable import ParametersTable
import json

class DelStu:
    def __init__(self, connection, parameters):
        self.connection = connection
        self.parameters = parameters

    def execute(self):
        name = self.parameters.get('name')
        StudentInfo = StudentInfoTable()
        Parameters = ParametersTable()
        stu_id = StudentInfo.select_a_student(name)
        if stu_id is None:
            response = {
                'status': 'Fail',
                'message': 'Name parameter is missing'
            }
            self.connection.send(json.dumps(response).encode())
        else:
            stu_id = stu_id[0]
            StudentInfo.delete_a_student(stu_id)
            Parameters.delete_a_subject(stu_id)                
            response_1 = {
                    'command': 'delete',
                    'parameters': {'name': name}
                }
            self.connection.send(json.dumps(response_1).encode())

            response_2 = {
                    'status': 'OK'
                }
            self.connection.send(json.dumps(response_2).encode())
            
