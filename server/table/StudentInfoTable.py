from DB.DBConnection import DBConnection

class StudentInfoTable:
    def insert_a_student(self, name):
        # Check if the student already exists
        existing_student = self.select_a_student(name)
        if existing_student:
            # Student already exists, handle accordingly
            return False  # Indicate failure
        else:
            # Student does not exist, proceed with insertion
            command = "INSERT INTO student_info (name) VALUES ('{}');".format(name)
            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                connection.commit()
            return True  # Indicate success


    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['stu_id'] for row in record_from_db]
    
    def select_all_students(self):
        command = "SELECT stu_id, name FROM student_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records_from_db = cursor.fetchall()

        student_names_dict = {record['name']:record['stu_id'] for record in records_from_db}

        return student_names_dict
    
    def get_student_info(self, stu_id):
        command = "SELECT * FROM student_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchone()

        student_info = dict(record_from_db)

        return student_info

    def delete_a_student(self, stu_id):
        command = "DELETE FROM student_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_student(self, stu_id, name):
        command = "UPDATE student_info SET name='{}' WHERE stu_id='{}';".format(name, stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
       