from PyQt6.QtCore import QThread, pyqtSignal
from client.SocketClient import SocketClient
import json

class ServiceController():

    def __init__(self):
        self.socket_client = SocketClient()

    def command_sender(self, command, data):
        self.socket_client.send_command(command, data)
        result = self.socket_client.wait_response()

        return result


class ExecuteCommand(QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, command, data):
        super().__init__()
        self.data = data
        self.command = command

    def run(self):
        result = ServiceController().command_sender(self.command, self.data)
        self.return_sig.emit(json.dumps(result))