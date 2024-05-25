class StudentClientHandler:
    def __init__(self, client, student_dict):
        self.client = client
        self.student_dict = student_dict
    
    def query_student(self):
        student_name = self.student_dict.get('name')
        if not student_name:
            return None

        self.client.send_command('query', {'name': student_name})
        _, response = self.client.wait_response()

        if response.get('status') == 'OK':
            print(f"Student {student_name} already exists.")
        return response

    def add_student(self, subject, score):
        response = self.query_student()
        if response and response.get('status') == 'OK':
            return False

        scores = self.student_dict.get('scores', {})
        scores[subject] = score
        self.student_dict['scores'] = scores

        self.client.send_command('add', {'name': self.student_dict.get('name'), 'scores': scores})
        keep_going, _ = self.client.wait_response()

        print(f"Add {self.student_dict.get('name')}'s {subject} score: {score} successfully.")
        return keep_going

    def show_students(self):
        self.client.send_command('show', {})
        keep_going, response = self.client.wait_response()
        print(response)
        return response

