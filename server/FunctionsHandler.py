import sys
sys.path.insert(0, '../sqlite')
from StudentInfoTable import StudentInfoTable

class FunctionsHandler:
    def __init__(self):
        self.students = StudentInfoTable()

    def add_student(self, parameters):
        student_name = parameters.get('name')
        student_scores = parameters.get('scores', {})

        if student_name is None:  
            return {'status': 'failed', 'message': 'Student name cannot be empty'}

        if self.students.select_a_student(student_name):
            return {'status': 'failed', 'message': f'Student {student_name} already exists'}

        self.students.insert_a_student(student_name)
        for subject, score in student_scores.items():
            self.students.add_a_student_score(student_name, subject, score)
        return {'status': 'OK', 'message': f'Student {student_name} added successfully'}

    def del_student(self, parameters):
        student_name = parameters.get('name')
        stu_id = self.students.select_a_student(student_name)
        if not stu_id:
            return {'status': 'failed', 'message': f'Student {student_name} not found'}

        self.students.delete_a_student(stu_id[0]) 
        return {'status': 'OK', 'message': f'Student {student_name} deleted successfully'}

    def modify_student(self, parameters):
        student_name = parameters.get('name')
        subject = parameters.get('subject')
        score = parameters.get('score')

        if not self.students.select_a_student(student_name):
            return {'status': 'failed', 'message': f'Student {student_name} not found'}

        self.students.update_student_score(student_name, subject, score)
        return {'status': 'OK', 'message': f"{student_name}'s score for {subject} modified successfully"}

    def show_students(self):
        all_students = self.students.select_all_students()

        if not all_students:
            return {'status': 'OK', 'parameters': {}}

        parameters = {}
        for student in all_students:
            student = dict(student)  
            student_name = student['name']
            scores = self.students.select_a_student_scores(student_name)
            scores = [dict(score) for score in scores]
            parameters[student_name] = {'scores': scores}

        return {'status': 'OK', 'parameters': parameters}

    def query_student(self, parameters):
        student_name = parameters.get('name')

        if not self.students.select_a_student(student_name):
            return {'status': 'failed', 'message': f'Student {student_name} not found'}

        scores = self.students.select_a_student_scores(student_name)
        scores = [dict(score) for score in scores]  
        parameters = {student_name: {'scores': scores}}
                
        return {'status': 'OK', 'parameters': parameters}

    def command_handler(self, message):
        command = message.get('command')
        parameters = message.get('parameters', {})
        
        command_func_map = {
            'add': (self.add_student, True),
            'del': (self.del_student, True),
            'modify': (self.modify_student, True),
            'show': (self.show_students, False),
            'query': (self.query_student, True)
        }

        func, needs_parameters = command_func_map.get(command, (None, False))
        
        if func is not None:
            if needs_parameters:
                if isinstance(parameters, bool):
                    parameters = {}
                return func(parameters)
            else:
                return func()
        else:
            return {'status': 'failed', 'message': 'Invalid command'}