from DB.DBConnection import DBConnection

class ParametersTable:

    def insert_a_subject(self, stu_id, subject, score):
        select_command = "SELECT * FROM subject_info WHERE stu_id='{}' AND subject='{}';".format(stu_id, subject)
        insert_command = "INSERT INTO subject_info (stu_id, subject, score) VALUES ('{}', '{}', '{}');".format(stu_id, subject, score)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(select_command)
            existing_record = cursor.fetchone()

            if existing_record:
                print("Record already exists for stu_id '{}' and subject '{}'.".format(stu_id, subject))
            else:
                cursor.execute(insert_command)
                connection.commit()
                print("New record inserted for stu_id '{}' and subject '{}' with score '{}'.".format(stu_id, subject, score))
        print("SQL command executed successfully.")

    def select_a_subject(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        
        dict = {row['subject'] : row['score'] for row in record_from_db}

        return dict

    def delete_a_subject(self, stu_id):
        command = "DELETE FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_subject(self, stu_id, subject, new_score):
        select_subject_command = "SELECT * FROM subject_info WHERE stu_id=? AND subject=?;"
        insert_score_command = "INSERT INTO subject_info (stu_id, subject, score) VALUES (?, ?, ?);"
        update_score_command = "UPDATE subject_info SET score=? WHERE stu_id=? AND subject=?;"

        with DBConnection() as connection:
            cursor = connection.cursor()

            # 檢查科目是否存在
            cursor.execute(select_subject_command, (stu_id, subject))
            existing_subject = cursor.fetchone()
            
            if not existing_subject:
                # 如果科目不存在，新增科目及成績
                cursor.execute(insert_score_command, (stu_id, subject, new_score))
                connection.commit()
                print("Inserted new record for stu_id '{}' and subject '{}' with score '{}'.".format(stu_id, subject, new_score))
            else:
                # 如果科目存在，則更新成績
                cursor.execute(update_score_command, (new_score, stu_id, subject))
                connection.commit()
                print("Updated score for stu_id '{}' and subject '{}' to '{}'.".format(stu_id, subject, new_score))

        print("SQL command executed successfully.")

