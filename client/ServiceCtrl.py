from PyQt6.QtCore import QThread, pyqtSignal
from client.SocketClient import SocketClient
from client.StudentClientHandler import StudentClientHandler

class ServiceCtrl(QThread):
    query_signal=pyqtSignal(dict)
    add_signal=pyqtSignal(dict)
    send_signal=pyqtSignal(dict)
    show_signal=pyqtSignal(dict) 
    
    def __init__(self):
        super().__init__()
        self.client = SocketClient("127.0.0.1", 20001)

    def query(self, name):
        student_handler = StudentClientHandler(self.client, {'name': name})
        response = student_handler.query_student()
        self.query_signal.emit(response)
        return response

    def show(self):
        student_handler = StudentClientHandler(self.client, {"name": ""})
        response = student_handler.show_students()
        self.show_signal.emit(response)
        print(response)
        return response

    def send(self, command, params):
        student_handler = StudentClientHandler(self.client, params)
        student_handler.client.send_command(command, params)
        response = self.client.wait_response()
        return response