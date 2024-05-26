from Commands.StudentInfoTable import StudentInfoTable

class PrintAll:

    def __init__(self, parameters):
        self.execute_result = {}

    def execute(self):
        students, scores = StudentInfoTable().get_data()
        scores_dict = {}
        for score in scores:
            stu_id = score['stu_id']
            if stu_id not in scores_dict:
                scores_dict[stu_id] = {}
            scores_dict[stu_id][score['subject']] = score['score']

        database = {}
        for student in students:
            student_name = student['name']
            database[student_name] = {
                'name': student_name,
                'scores': scores_dict.get(student['stu_id'], {})
            }

        self.execute_result = {'status': 'OK', 'parameters': database}

        return self.execute_result
    
if __name__ == '__main__':
    from DBController.DBConnection import DBConnection
    from DBController.DBInitializer import DBInitializer

    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()
    print(PrintAll().execute()) 
