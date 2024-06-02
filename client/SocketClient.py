import socket 
import json

class SocketClient:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 20001
        self.BUFFER_SIZE = 1940
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client_socket.connect((self.host, self.port))       

    def send_command(self, command, parameters=None):
        if parameters is None:
            parameters = {}
        send_data = {'command': command, 'parameters': parameters}
        self.client_socket.send(json.dumps(send_data).encode())

    def wait_response(self):
        data = self.client_socket.recv(self.BUFFER_SIZE)
        raw_data = data.decode()
        print("The client received data => ", raw_data)
        if raw_data == "closing":
            return False        
        try:
            response = json.loads(raw_data)
            return response
        except json.JSONDecodeError:
            print("Error decoding JSON:", raw_data)
            return False
 
