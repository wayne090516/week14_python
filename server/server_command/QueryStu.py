from table.StudentInfoTable import StudentInfoTable
from table.ParametersTable import ParametersTable
import json

class QueryStu:
    def __init__(self, connection, parameters):
        self.connection = connection
        self.parameters = parameters

    def execute(self):
        name = self.parameters.get('name')
        StudentInfo = StudentInfoTable()
        Parameters = ParametersTable()
        stu_ids = StudentInfo.select_a_student(name)

        if not stu_ids:
            response = {
                'status': 'Fail',
                'reason': 'The name is not found.'
            }
        else:
            stu_id = stu_ids[0]
            scores = Parameters.select_a_subject(stu_id)
            response = {
                'status': 'OK',
                'scores': scores
            }       
        self.connection.send(json.dumps(response).encode())
