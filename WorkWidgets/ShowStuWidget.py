from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ScrollableLabelComponent
from socket_cli.Control import ExecuteCommand
from socket_cli.Socket_cli import SocketClient
import time


class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent(20, "Show Student")
        self.scrollable_label = ScrollableLabelComponent(12, "")
        layout.addWidget(header_label)
        layout.addWidget(self.scrollable_label)
        self.setLayout(layout)
        self.client = SocketClient()

    
    def load(self):
        executecommand=ExecuteCommand(self.client, "show", "")
        executecommand.return_sig.connect(self.printall)
        executecommand.run()

    def printall(self,received_data):
        student_dict=eval(received_data)
        student_dict= student_dict["parameters"]
        stu_str=""
        for key in student_dict:
            stu_str+=(f"Name: {key}\n")
            score=student_dict[key]
            for subject in score:
                stu_str+=("  subject: {}, score: {}\n".format(subject,score[subject]))
            stu_str+=("\n")
        print(stu_str)
        self.scrollable_label.set_text(stu_str)
