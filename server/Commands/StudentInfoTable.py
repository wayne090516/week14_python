from DBController.DBConnection import DBConnection

class StudentInfoTable:
    def insert_a_student(self, parameters):
        command = "INSERT INTO student_info (name) VALUES  ('{}');".format(parameters['name'])
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['stu_id'] for row in record_from_db]

    def delete_a_student(self, stu_id):
        student_info_command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)
        subject_info_command = "DELETE FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(student_info_command)
            cursor.execute(subject_info_command)
            connection.commit()

    def update_a_student(self, stu_id, name):
        command = "UPDATE student_info SET name='{}' WHERE stu_id='{}';".format(name, stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def get_data(self):
        student_info_command = "SELECT * FROM student_info;"
        subject_info_command = "SELECT * FROM subject_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            
            cursor.execute(student_info_command)
            students = cursor.fetchall()
            
            cursor.execute(subject_info_command)
            scores = cursor.fetchall()
        
        return students, scores