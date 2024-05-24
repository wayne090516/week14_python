from sqlite_example.StudentInfoTable import StudentInfoTable
class Query:
    def __init__(self, message, connection):
        self.connection = connection
        self.parameters = message['parameters']

    def execute(self):
        name=self.parameters['name']
        student_info_table = StudentInfoTable()
        stu_id = student_info_table.select_a_student(name)
        if stu_id != []: 
            reply_msg = str({'status': 'OK', 'reason': self.parameters})
            print(reply_msg)
            self.connection.send(reply_msg.encode())
        else:
            reply_msg = "{'status': 'Fail', 'reason': 'The name is not found.'}"
            print(reply_msg)
            self.connection.send(reply_msg.encode())