from Commands.StudentInfoTable import StudentInfoTable
from Commands.SubjectInfoTable import SubjectInfoTable

class AddStu:

    def __init__(self, parameters):
        self.parameters = parameters
        self.execute_result = {}

    def execute(self):
        StudentInfoTable().insert_a_student(self.parameters)
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]
        SubjectInfoTable().insert_subject_info(stu_id, self.parameters)
        
        self.execute_result = {'status':'OK'}
        print(f"    Add {self.parameters['name']} success")

        return self.execute_result
    
if __name__ == '__main__':
    from DBController.DBConnection import DBConnection
    from DBController.DBInitializer import DBInitializer

    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()
    para = {'name': 'test', 'scores': {'English': 99.0, 'Chinese': 88.0}}
    AddStu(para).execute()