from threading import Thread
import socket
import json

host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, job_dispatcher):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.job_dispatcher = job_dispatcher

    def serve(self):
        self.start()

    def run(self):
        while True:
            try:
                connection, address = self.server_socket.accept()
                print("{} connected".format(address))
                self.new_connection(connection=connection, address=address)
            except Exception as e:
                pass

    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
                                kwargs={"connection": connection, "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            
            try:
                message = connection.recv(1024).strip().decode()
            except:
                keep_going = False
            else:
                if not message:
                    break
                message = json.loads(message)
                print("    server received:{} from {}".format(message,address))
                execute_result = self.job_dispatcher.job_execute(message['command'], message['parameters'])
                connection.send(json.dumps(execute_result).encode())
        
        connection.close()
        print("{} close connection".format(address))

if __name__ == '__main__':
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")
