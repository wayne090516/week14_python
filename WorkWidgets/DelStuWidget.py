from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ScrollableLabelComponent, ComboBoxComponent
from socket_cli.Control import ExecuteCommand
from socket_cli.Socket_cli import SocketClient
import time


class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Del_stu_widget")

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)
        layout.setRowStretch(2, 1)

        header_label = LabelComponent(20, "Delete Student")
        self.scrollable_label = ScrollableLabelComponent(12, "")
        self.combobox = ComboBoxComponent()
        
        self.button_del = ButtonComponent("Del")
        self.button_del.clicked.connect(self.del_stu)

        layout.addWidget(header_label,0,0,1,2)
        layout.addWidget(self.scrollable_label,1,0,1,2)
        layout.addWidget(self.combobox,2,0,1,1)
        layout.addWidget(self.button_del,2,1,1,1)
        self.setLayout(layout)
        self.client = SocketClient()

    
    def load(self):
        self.combobox.clear()
        executecommand=ExecuteCommand(self.client, "show", "")
        executecommand.return_sig.connect(self.printall)
        executecommand.run()

    def del_stu(self):
        if self.combobox.currentText()!="":
            executecommand=ExecuteCommand(self.client, "del", {"name":self.combobox.currentText()})
            executecommand.return_sig.connect(self.load)
            executecommand.run()

    def printall(self,received_data):
        student_dict=eval(received_data)
        student_dict=student_dict["parameters"]
        stu_str=""
        for key in student_dict:
            self.combobox.addItem(key)
            stu_str+=(f"Name: {key}\n")
            score=student_dict[key]
            for subject in score:
                stu_str+=("  subject: {}, score: {}\n".format(subject,score[subject]))
            stu_str+=("\n")
        print(stu_str)
        self.scrollable_label.set_text(stu_str)
