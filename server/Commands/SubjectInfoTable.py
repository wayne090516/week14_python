from DBController.DBConnection import DBConnection

class SubjectInfoTable:

    def insert_subject_info(self, stu_id, parameters):
        command = "INSERT INTO subject_info (stu_id, subject, score) VALUES (?, ?, ?);"
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            for subject, score in parameters['scores'].items():
                cursor.execute(command, (int(stu_id), str(subject), float(score)))
            connection.commit()

    def select_subject_info(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return {row['subject'] : row['score'] for row in record_from_db}

    def update_subject_info(self, stu_id, subject, new_score):
        command = "SELECT * FROM subject_info WHERE stu_id='{}' AND subject='{}';".format(stu_id, subject)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            exist = cursor.fetchone()

        if exist:
            command = "UPDATE subject_info SET score='{}' WHERE stu_id='{}' AND subject='{}';".format(new_score, stu_id, subject)
        else:
            command = "INSERT INTO subject_info (stu_id, subject, score) VALUES ('{}', '{}', '{}');".format(stu_id, subject, new_score)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()