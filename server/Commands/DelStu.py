from Commands.StudentInfoTable import StudentInfoTable

class DelStu:

    def __init__(self, parameters):
        self.parameters = parameters
        self.execute_result = {}

    def execute(self):
        stu_id = StudentInfoTable().select_a_student(self.parameters['name'])[0]
        StudentInfoTable().delete_a_student(stu_id)
        self.execute_result = {'status':'OK'}
        print(f"    Del {self.parameters['name']} success")

        return self.execute_result

if __name__ == '__main__':
    from DBController.DBConnection import DBConnection
    from DBController.DBInitializer import DBInitializer

    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()
    print(DelStu({'name': 'test'}).execute()) 