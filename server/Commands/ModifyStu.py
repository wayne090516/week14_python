from Commands.StudentInfoTable import StudentInfoTable
from Commands.SubjectInfoTable import SubjectInfoTable

class ModifyStu:

    def __init__(self, parameters):
        self.parameters = parameters
        self.execute_result = {}

    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]
        for subject, score in self.parameters['scores'].items():
            SubjectInfoTable().update_subject_info(stu_id, subject, score)
            show_data = [self.parameters['name'], subject, score]
            
        self.execute_result = {'status': 'OK'}
        print(f"    Modify {show_data} success")

        return self.execute_result

if __name__ == '__main__':
    from DBController.DBConnection import DBConnection
    from DBController.DBInitializer import DBInitializer

    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()
    para = {'name': 'test', 'scores': {'English': 99.0, 'Chinese': 88.0}}
    print(ModifyStu(para).execute()) 