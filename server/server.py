from threading import Thread
import socket
import json
from FunctionsHandler import FunctionsHandler
import sys
sys.path.insert(0, '../sqlite')
from DBConnection import DBConnection
from DBInitializer import DBInitializer


host = "127.0.0.1"
port = 20001

class SocketServer(Thread):
    def __init__(self, host, port, handler):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.handler = handler

    def serve(self):
        self.start()

    def run(self):
        while True:
            connection, address = self.server_socket.accept()
            print("{} connected".format(address))
            self.new_connection(connection=connection,
                                address=address)


    def new_connection(self, connection, address):
        Thread(target=self.receive_message_from_client,
               kwargs={
                   "connection": connection,
                   "address": address}, daemon=True).start()

    def receive_message_from_client(self, connection, address):
        keep_going = True
        while keep_going:
            try:
                message = connection.recv(1024).strip().decode()
                if message:
                    message = json.loads(message)
                    print("server received: {} from {}".format(message, address)) 
                else:
                    continue
            except Exception as e:
                print("Exception happened {}, {}".format(e, address))
                keep_going = False
            else:
                if message:
                    if message['command'] == "exit":
                        connection.send("exit".encode())
                        keep_going = False
                    else:
                        response = self.handler.command_handler(message)
                        reply_msg = json.dumps(response)
                        connection.send(reply_msg.encode())
                else:
                    keep_going = False

        connection.close()
        print("{} close connection".format(address))


if __name__ == '__main__':
    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()

    functions_handler = FunctionsHandler()
    server = SocketServer(host, port, functions_handler)
    server.daemon = True
    server.serve()
    print("\nWelcome!\n")
    while True:
        command = input()
        if command.lower() == 'close':
            print("\nThank for using.\n")
            break

    server.server_socket.close()
    print("leaving ....... ")
