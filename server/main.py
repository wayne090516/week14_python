from Commands.AddStu import AddStu
from Commands.DelStu import DelStu
from Commands.ModifyStu import ModifyStu
from Commands.PrintAll import PrintAll
from Commands.QueryStu import QueryStu
from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from SocketServer.SocketServer import SocketServer

action_list = {
    "add": AddStu, 
    "del": DelStu,
    "modify": ModifyStu,
    "show": PrintAll,
    "query": QueryStu
}

class JobDispatcher:

    def job_execute(self, command, parameters):
        execute_result = action_list[command](parameters).execute()
        return execute_result

def main():
    DBConnection.db_file_path = "student_data.db"
    DBInitializer().execute()

    job_dispatcher = JobDispatcher()
    server = SocketServer(job_dispatcher)
    server.daemon = True
    server.serve()

    print("Welcome! ＜(´⌯ w ⌯`)＞")
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")

if __name__ == "__main__":
    main()