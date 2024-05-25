from DBConnection import DBConnection


class StudentInfoTable:
    def insert_a_student(self, name):
        command = "INSERT INTO student_info (name) VALUES  ('{}');".format(name)
            
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
        command = "DELETE FROM subject_info WHERE stu_id = {};".format(stu_id)
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

        command = "DELETE FROM student_info WHERE stu_id = {};".format(stu_id)
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

    def add_a_student_score(self, student_name, subject, score):
        stu_id = self.select_a_student(student_name)
        if stu_id:
            command = "INSERT INTO subject_info (stu_id, subject, score) VALUES  ({}, '{}', {});".format(stu_id[0], subject, score)
            
            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                connection.commit()
        else:
            print("Student not found.")

    def select_a_student_scores(self, student_name):
        stu_id = self.select_a_student(student_name)
        if stu_id:
            command = "SELECT subject, score FROM subject_info WHERE stu_id={};".format(stu_id[0])
                
            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                records_from_db = cursor.fetchall()

            return records_from_db
        else:
            print("Student not found.")
            return None

    def select_all_students(self):
        command = "SELECT * FROM student_info"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            records_from_db = cursor.fetchall()

        return records_from_db

    def update_student_score(self, student_name, subject, score):
        stu_id = self.select_a_student(student_name)
        if stu_id:
            command = "UPDATE subject_info SET score = {} WHERE stu_id = {} AND subject = '{}';".format(score, stu_id[0], subject)
            with DBConnection() as connection:
                cursor = connection.cursor()
                cursor.execute(command)
                connection.commit()
        else:
            print("Student not found.")