from sqlite_example.StudentInfoTable import StudentInfoTable
from sqlite_example.SubjectInfoTable import SubjectInfoTable
class AddStu:
    def __init__(self, message, connection):
        self.connection = connection
        self.parameters = message['parameters']

    def execute(self):
        name=self.parameters['name']
        subject_info_table = SubjectInfoTable()
        student_info_table = StudentInfoTable()
        stu_id = student_info_table.select_a_student(name)
        if stu_id == []: 
            
            student_info_table.insert_a_student(name)
            stu_id = student_info_table.select_a_student(name)[0]

            for subject, score in self.parameters['scores'].items():
                subject_info_table.insert_subject_info(stu_id, subject, score)
                
            reply_msg = str({'status': 'OK', 'reason': self.parameters})
            print(reply_msg)
            self.connection.send(reply_msg.encode())
        else:
            reply_msg = str({'status': 'Fail', 'reason': self.parameters})
            print(reply_msg)
            self.connection.send(reply_msg.encode())