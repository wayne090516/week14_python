from table.StudentInfoTable import StudentInfoTable
from table.ParametersTable import ParametersTable
import json

class AddStu:
    def __init__(self, connection, parameters):
        self.connection = connection
        self.parameters = parameters

    def execute(self):
        name = self.parameters.get('name')
        scores = self.parameters.get('scores', {})
        StudentInfo = StudentInfoTable()
        Parameters = ParametersTable()

        existing_stu = StudentInfo.select_a_student(name)       
        if existing_stu:
            response = {'status': 'Fail', 'reason': 'The name already exists.'}
        else:
            StudentInfo.insert_a_student(name)
            new_stu_id = StudentInfo.select_a_student(name)
            if new_stu_id:
                stu_id = new_stu_id[0]
                for subject, score in scores.items():
                    Parameters.insert_a_subject(stu_id, subject, score)
                response = {'status': 'OK'}
            else:
                response = {'status': 'Fail', 'reason': 'Failed to retrieve student ID.'}
        
        self.connection.send(json.dumps(response).encode())


