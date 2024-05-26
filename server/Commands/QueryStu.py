from Commands.StudentInfoTable import StudentInfoTable
from Commands.SubjectInfoTable import SubjectInfoTable

class QueryStu:

    def __init__(self, parameters):
        self.parameters = parameters
        self.execute_result = {}

    def execute(self):
        if StudentInfoTable().select_a_student(self.parameters['name']):
            stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]
            scores = SubjectInfoTable().select_subject_info(stu_id)
            self.execute_result = {'status': 'OK', 'scores': scores}
        else:
            self.execute_result = {'status': 'Fail', 'reason': 'The name is not found.'}
        print(f"    Query {self.parameters['name']} success")

        return self.execute_result
    
if __name__ == '__main__':
    from DBController.DBConnection import DBConnection
    from DBController.DBInitializer import DBInitializer

    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()
    print(QueryStu({'name': 'Test'}).execute())
