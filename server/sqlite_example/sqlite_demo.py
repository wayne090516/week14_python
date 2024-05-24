from DBConnection import DBConnection
from DBInitializer import DBInitializer
from StudentInfoTable import StudentInfoTable


DBConnection.db_file_path = "example.db"
DBInitializer().execute()

#StudentInfoTable().insert_a_student("Bill")
#StudentInfoTable().insert_a_student("John")
#StudentInfoTable().insert_a_student("Joe")


student_id = StudentInfoTable().select_a_student("Joe")
print("student_id: {}".format(student_id))

student_id = StudentInfoTable().select_a_student("Bill")
print("student_id: {}".format(student_id))
student_id=1
StudentInfoTable().delete_a_student(student_id)

student_id = StudentInfoTable().select_a_student("Bill")
print("student_id: {}".format(student_id))
print(type(student_id))

# StudentInfoTable().update_a_student("1", "Test")
