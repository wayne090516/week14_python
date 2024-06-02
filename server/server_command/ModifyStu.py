from table.StudentInfoTable import StudentInfoTable
from table.ParametersTable import ParametersTable
import json


class ModifyStu:
    def __init__(self, connection, parameters):
        self.connection = connection
        self.parameters = parameters

    def execute(self):
        name = self.parameters.get('name')
        StudentInfo = StudentInfoTable()
        Parameters = ParametersTable()
        stu_id = StudentInfo.select_a_student(name)

        if not stu_id:
            response = {'status': 'Fail', 'reason': 'The name is not found.'}
        else:
            stu_id = stu_id[0]
            scores_dict = self.parameters.get('scores_dict', {})
            
            for subject, score in scores_dict.items():
                Parameters.update_a_subject(stu_id, subject, score)
                                                    
        response = {'status': 'OK'}       
        self.connection.send(json.dumps(response).encode())

            
