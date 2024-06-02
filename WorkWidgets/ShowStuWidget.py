from PyQt6 import QtWidgets
from WorkWidgets.WidgetComponents import LabelComponent, ScrollComponent
from client.ServiceControl import ExecuteCommand
from client.SocketClient import SocketClient
import json

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        self.scrollable_label = ScrollComponent(12, "")
        layout.addWidget(self.scrollable_label)
        self.setLayout(layout)
        self.client = SocketClient()

    def load(self):
        print("show widget")
        self.execute_show = ExecuteCommand("show", {})
        self.execute_show.return_sig.connect(self.show_all) 
        self.execute_show.start()
               

    def show_all(self,received_data):
        try:
            student_dict = json.loads(received_data)
            student_dict = student_dict.get("parameters", {})
            stu = "\n==== student list ====\n"
            for name, scores in student_dict.items():
                stu += (f"Name: {name}\n")
                for subject, score in scores.items():
                    stu += (f"  subject: {subject}, scores: {score}\n")
                stu += ("\n")
            stu += "======================"
            print(stu)
            self.scrollable_label.set_text(stu)
        except json.JSONDecodeError as e:
            self.scrollable_label.set_text("Failed to load student data.")
        except Exception as e:
            self.scrollable_label.set_text("An error occurred while loading student data.")