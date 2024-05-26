from PyQt6 import QtWidgets, QtGui
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.ServiceController import ExecuteCommand
import json

from PyQt6.QtWidgets import QApplication
import sys


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("add_stu_widget")
        self.setWindowTitle("Add Student")
        self.setFixedSize(400, 300)

        layout = QtWidgets.QGridLayout()

        # Header, Name and Query-button
        # header_label = LabelComponent(20, "Add Student")
        content_label_name = LabelComponent(16, "Name: ", alignment="left")
        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_entered)
        layout.addWidget(content_label_name, 0, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 0, 1, 1, 2)

        self.button_query = ButtonComponent("Check")
        self.button_query.clicked.connect(self.query_pressed)
        self.button_query.setEnabled(False)
        layout.addWidget(self.button_query, 0, 3, 1, 2)

        # layout.addWidget(header_label, 0, 0, 1, 2)

        # Subject and Add-button
        content_label_subject = LabelComponent(16, "Subject: ", alignment="left")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_subject.setEnabled(False)
        layout.addWidget(content_label_subject, 1, 0, 1, 1)
        layout.addWidget(self.editor_label_subject, 1, 1, 1, 2)

        self.button_add = ButtonComponent("Add")
        self.button_add.clicked.connect(self.add_pressed)
        self.button_add.setEnabled(False)
        layout.addWidget(self.button_add, 1, 3, 1, 2)


        # Score and Send-button
        content_label_score = LabelComponent(16, "Score: ", alignment="left")
        self.editor_label_score = LineEditComponent("Score")
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.setEnabled(False)
        self.editor_label_score.setValidator(QtGui.QIntValidator(0, 100)) # QtGui.QIntValidator(min_value, max_value)
        self.editor_label_score.textChanged.connect(self.score_entered)
        layout.addWidget(content_label_score, 2, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 2, 1, 1, 2)

        self.button_send = ButtonComponent("Send")
        self.button_send.clicked.connect(self.send_pressed)
        layout.addWidget(self.button_send, 2, 3, 1, 2)
        self.button_send.setEnabled(False)

        # Respond-window 
        self.respond_window = LabelComponent(16, content="", alignment="left", bg_color="", style="red")
        self.respond_window.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.respond_window, 3, 0, 1, 5)
        

        # Set Layouts
        for i in range(5):
            layout.setColumnStretch(i, 1)
        for i in range(4):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

    def load(self):
            self.respond_window.setText("")
            self.editor_label_name.setText("Name")
            self.editor_label_subject.setText("Subject")
            self.editor_label_score.setText("Score")
            self.editor_label_name.setEnabled(True)
            self.editor_label_subject.setEnabled(False)
            self.editor_label_score.setEnabled(False)
            self.button_query.setEnabled(False)
            self.button_add.setEnabled(False)
            self.button_send.setEnabled(False)
            self.scores_dict = dict()
            print("add widget")

    def query_pressed(self):
        self.button_query.setEnabled(False)
        self.name = self.editor_label_name.text()
        query_data = {"name": self.name}
        self.execute_query = ExecuteCommand(command="query", data=query_data)
        self.execute_query.start()
        self.execute_query.return_sig.connect(self.query_action_result)

    def query_action_result(self, result):
        status = eval(json.loads(result))["status"]

        if status == "Fail":
            self.editor_label_name.setEnabled(False)
            self.editor_label_subject.setEnabled(True)
            self.editor_label_score.setEnabled(True)
        elif status == "OK":
            self.editor_label_name.setText("Name")

    def add_pressed(self):
        self.scores_dict = {}
        if (self.editor_label_name.text()=="" or self.editor_label_subject.text()=="" or self.editor_label_score.text()==""):
            self.respond_window.setText("Please enter the subject and score for the student")
        else:
            self.button_send.setEnabled(True)
            self.scores_dict[self.editor_label_subject.text()] = self.editor_label_score.text()
            self.parameters = {'name': self.name, 'scores': self.scores_dict}
            self.respond_window.setText(f"{self.parameters} added")

    def send_pressed(self):
        if (self.editor_label_name.text() ==""or self.editor_label_subject.text() =="" or self.editor_label_score.text() ==""):
            self.respond_window.setText("Please enter the subject and score for the student")
        else:
            send_data = self.parameters
            self.execute_send = ExecuteCommand(command="add", data=send_data)
            self.execute_send.start()
            self.execute_send.return_sig.connect(self.send_action_result)

    def send_action_result(self, result):
        status = eval(json.loads(result))["status"]

        if status == "Fail":
            self.respond_window.setText("Add " + str(self.parameters) + " failed!")
        elif status == "OK":
            self.respond_window.setText("Add " + str(self.parameters) + " successfully!")
            # Preset
            self.load()

    def name_entered(self):
        if self.editor_label_name.text() != "":
            self.button_query.setEnabled(True)
    
    def score_entered(self):
        if self.editor_label_score.text() != "":
            self.button_add.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    main_window = AddStuWidget()
    main_window.show()

    sys.exit(app.exec())
