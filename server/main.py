from socket_sever import SocketServer
from sel_fuc.AddStu import AddStu
from sel_fuc.PrintAll import PrintAll
from sel_fuc.DelStu import DelStu
from sel_fuc.Query import Query
from sel_fuc.ModifyStu import Modify
from sqlite_example.DBConnection import DBConnection
from sqlite_example.DBInitializer import DBInitializer

action_list = {
    "add": AddStu, 
    "del": DelStu, 
    "query" : Query,
    "modify": Modify, 
    "show": PrintAll
}

def message_sel(message,connection):
    select_result = message['command']
    action_list[select_result](message,connection).execute()

if __name__ == '__main__':
    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()

    server = SocketServer(message_sel)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")