from threading import Thread
from server_command.AddStu import AddStu
from server_command.PrintAll import PrintAll
from server_command.DelStu import DelStu
from server_command.ModifyStu import ModifyStu
from server_command.QueryStu import QueryStu
from DB.DBConnection import DBConnection
from DB.DBInitializer import DBInitializer
import socket
import json

host = "127.0.0.1"
port = 20001

action_list = {
    "add" : AddStu,
    "del" : DelStu,
    "modify" : ModifyStu,    
    "show" : PrintAll,
    "query" : QueryStu
}

class SocketServer(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The following setting is to avoid the server crash. So, the binded address can be reused
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
              

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
            except Exception as e:
                print("Exeption happened {}, {}".format(e, address))
                keep_going = False
            else:
                if not message:
                    keep_going = False
                print("server received:", message, "from", address)
                
                try:
                    message = json.loads(message)
                except json.JSONDecodeError as e:
                    print("JSON decode error:", e)
                    continue

                command = message.get('command')
                parameters = message.get('parameters')

                if command in action_list:
                    self.student_dict = action_list[command](connection, parameters).execute()
                else:
                    print("Unknown command:", command)

        connection.close()
        print("{} close connection".format(address))


if __name__ == '__main__':
    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()
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
