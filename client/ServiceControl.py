from PyQt6.QtCore import pyqtSignal
from client.SocketClient import SocketClient
from PyQt6 import QtCore
import json

class ServiceControl:
    def __init__(self):
        self.socket_client = SocketClient()

    def command_sender(self, command, data):
        if self.socket_client is None:
            raise ValueError("Socket client is not set")
        self.socket_client.send_command(command, data)
        result = self.socket_client.wait_response()

        return result
    
class ExecuteCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, command, data):
        super().__init__()
        self.data = data
        self.command = command
        self.service_ctrl = ServiceControl()
    def run(self):
        result = self.service_ctrl.command_sender(self.command, self.data)
        self.return_sig.emit(json.dumps(result))