from sqlite_example.StudentInfoTable import StudentInfoTable
from sqlite_example.SubjectInfoTable import SubjectInfoTable

class PrintAll:
    def __init__(self, message, connection):
        self.connection = connection

    def execute(self):
        student_dict=dict()
        subject_info_table = SubjectInfoTable()
        student_info_table = StudentInfoTable()
        name_dic=student_info_table.select_all_students()
        for name, id in name_dic.items():
            student_dict[name]=subject_info_table.select_subject_info(id)
            print(student_dict)
        reply_msg = "{'status': 'OK', 'parameters': "+str(student_dict) +"}"
        self.connection.send(reply_msg.encode())