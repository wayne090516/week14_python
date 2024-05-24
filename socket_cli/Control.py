from socket_cli.AddStu import AddStu
from socket_cli.Query import Query
from PyQt6.QtCore import QThread, pyqtSignal
from socket_cli.Socket_cli import SocketClient
import json

class ExecuteCommand(QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, client, command, data):
        super().__init__()
        self.data = data
        self.command = command
        self.client=client

    def run(self):
        self.client.send_command(self.command, self.data )
        result = self.client.wait_response()
        self.return_sig.emit(result)

