from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from client.ServiceControl import ExecuteCommand
from PyQt6.QtCore import pyqtSignal
import json


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.add_dict = {}
        self.int_ui()

    def int_ui(self):
        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(19, "Add editor")
        content_label_name = LabelComponent(16, "Name: ")
        content_label_subject = LabelComponent(16, "Subject: ")
        content_label_score = LabelComponent(16, "Score: ")
        self.content_label_response = LabelComponent(16, "", "color:red;")

        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_score = LineEditComponent()
        self.editor_label_score.setValidator(QtGui.QIntValidator())
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_inputed)
        self.editor_label_score.textChanged.connect(self.score_inputed)
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)

        self.button_query = ButtonComponent("Query")
        self.button_add = ButtonComponent("Add")
        self.button_send = ButtonComponent("Send")
        self.button_query.clicked.connect(self.query)
        self.button_add.clicked.connect(self.add)
        self.button_send.clicked.connect(self.send)
        self.button_query.setEnabled(False)
        self.button_add.setEnabled(False)        

        layout.addWidget(self.button_send, 0, 4, 3, 3)
        layout.addWidget(content_label_name, 0, 0, 1, 1)
        layout.addWidget(content_label_subject, 1, 0, 1, 1)
        layout.addWidget(content_label_score, 2, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 0, 1, 1, 1)
        layout.addWidget(self.editor_label_subject, 1, 1, 1, 1)
        layout.addWidget(self.editor_label_score, 2, 1, 1, 1)
        layout.addWidget(self.button_query, 0, 2, 1, 1)
        layout.addWidget(self.button_add, 2, 2, 1, 1)
        layout.addWidget(self.content_label_response, 3, 0, 2, 4)

        self.button_send.setFixedSize(90, 150)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 3)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)

        self.setLayout(layout)

    def load(self):
        print("add widget")
        self.editor_label_name.setText("Name")
        self.editor_label_subject.setText("Subject")
        self.editor_label_score.setText("")
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)
        self.button_query.setEnabled(False)
        self.button_add.setEnabled(False)
        self.add_dict = dict()

    def name_inputed(self):
        self.button_query.setEnabled(bool(self.editor_label_name.text()))
        self.editor_label_score.setText("")
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setEnabled(False)
        self.button_add.setEnabled(False)        

    def score_inputed(self):
        self.button_add.setEnabled(bool(self.editor_label_score.text()))

    def query(self):
        name = self.editor_label_name.text()
        self.content_label_response.setText("The name has been changed.")
        self.query_thread = ExecuteCommand("query", {"name": name})
        self.query_thread.return_sig.connect(self.query_result)
        self.query_thread.start()
    
    def query_result(self,response_str):
        response = json.loads(response_str)
        if response["status"]=="Fail":
            self.editor_label_subject.setEnabled(True)
            self.editor_label_score.setEnabled(True)
        else:
            self.content_label_response.setText(f"The name is already exist.")

    def add(self):
        name = self.editor_label_name.text()
        subject = self.editor_label_subject.text()
        score = self.editor_label_score.text()
        if not subject or subject == "Subject" or not score:
            self.content_label_response.setText("Please input valid data.")
            return
        self.add_dict[self.editor_label_subject.text()] = self.editor_label_score.text()
        self.parameters = {'name': name, 'scores': self.add_dict}
        self.content_label_response.setText(f"The information {self.parameters} has been added.")

    def send(self):
        if not self.validate_inputs():
            return
        parameters = self.parameters
        self.send_thread = ExecuteCommand("add", parameters)
        self.send_thread.return_sig.connect(self.send_result)
        self.send_thread.start()   
    
    def send_result(self,response_str):
        response = json.loads(response_str)
        if response['status'] == "OK":
            self.editor_label_name.setText("Name")
            self.editor_label_subject.setText("Subject")
            self.editor_label_score.setText("")
            self.editor_label_subject.setEnabled(False)
            self.editor_label_score.setEnabled(False)
            self.button_query.setEnabled(False)
            self.button_add.setEnabled(False)
            self.add_dict = dict()
            name = self.parameters.get("name", "Unknown")
            scores = self.parameters.get("scores", {})
            subject = ", ".join([f"{key}: {value}" for key, value in scores.items()])
            self.content_label_response.setText(f"The student {name}'s subject {subject} added.")
        else:
             self.content_label_response.setText("Fail to add student.")
    
    def validate_inputs(self):
        name = self.editor_label_name.text()
        subject = self.editor_label_subject.text()
        score = self.editor_label_score.text()
        if not name or not subject or not score:
            self.content_label_response.setText("Please fill in all fields.")
            return False
        return True
    
