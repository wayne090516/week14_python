from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from client.ServiceControl import ExecuteCommand
from client.SocketClient import SocketClient
import json

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("mod_stu_widget")

        layout = QtWidgets.QGridLayout()

        content_label_name = LabelComponent(16, "Name: ")
        content_label_subject = LabelComponent(16, "Subject: ")
        content_label_score = LabelComponent(16, "Score: ")
        self.content_label_response = LabelComponent(16, "", "color:red;")

        self.name_combobox = ComboBoxComponent()
        self.sub_combobox = ComboBoxComponent()
       
        self.editor_label_newsubject = LineEditComponent("Subject")
        self.editor_label_score = LineEditComponent()
        self.editor_label_newsubject = LineEditComponent()     
        
        self.button_send = ButtonComponent("Send")

        self.name_combobox.currentTextChanged.connect(self.name_change)        
        self.sub_combobox.currentTextChanged.connect(self.subject_change)        
        self.button_send.clicked.connect(self.send) 

        self.editor_label_newsubject.mousePressEvent = self.editor_label_newsubject.clear_editor_content
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content

        self.editor_label_score.setValidator(QtGui.QIntValidator())

        self.editor_label_newsubject.setEnabled(False)

        layout.addWidget(content_label_name, 0, 0, 1, 1)
        layout.addWidget(self.button_send, 0, 3, 4, 2)
        layout.addWidget(self.name_combobox, 0, 1, 1, 1)
        layout.addWidget(content_label_subject, 1, 0, 1, 1)
        layout.addWidget(self.sub_combobox, 1, 1, 1, 1)
        layout.addWidget(self.editor_label_newsubject, 2, 1, 1, 1)        
        layout.addWidget(content_label_score, 3, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 1)
        layout.addWidget(self.content_label_response, 4, 0, 1, 5)
        
        
        self.button_send.setFixedSize(100, 150)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        self.setLayout(layout)

        self.client = SocketClient()

    def load(self):
        self.name_combobox.clear()
        self.sub_combobox.clear()
        self.editor_label_newsubject.setEnabled(False)
        self.editor_label_score.setText("")
        executecommand = ExecuteCommand("show", {})
        executecommand.return_sig.connect(self.stu_dict)
        executecommand.run()
   
    def stu_dict(self,received_data):
        student_dict = json.loads(received_data)
        self.student_dict = student_dict.get("parameters", {})
        for key in self.student_dict:
            self.name_combobox.addItem(key)

    def name_change(self):
        if self.name_combobox.currentText() != "":
            self.sub_combobox.clear()
            self.editor_label_newsubject.setText("Subject")
            self.editor_label_score.setText("") 

            score_dict = self.student_dict[self.name_combobox.currentText()]
            self.sub_combobox.addItem("add new subject")

            for key in score_dict:
                self.sub_combobox.addItem(key)
            self.editor_label_newsubject.setEnabled(True)
            
    def subject_change(self):
        if self.sub_combobox.currentText() != "add new subject":
            self.editor_label_newsubject.setEnabled(False)
        else:
            self.editor_label_newsubject.setEnabled(True)


    def send(self):
        self.stu_name = self.name_combobox.currentText()
        self.sub_name = self.sub_combobox.currentText()
        self.newsub_name = self.editor_label_newsubject.text()
        self.score_name = self.editor_label_score.text()
        
        if self.stu_name == "" or self.editor_label_score.text() == "" or (self.sub_name == "add new subject" and self.newsub_name == ""):
            self.content_label_response.setText("Please enter information.")
            return 0
        if self.stu_name in self.student_dict and self.sub_name in self.student_dict[self.stu_name]:
            scores = str(int(self.student_dict[self.stu_name][self.sub_name]))
            #print("*")
            #print(scores)
            #print(self.score_name)
            if self.score_name == scores:
                #print("**")
                self.content_label_response.setText("This data already exists.")
                return 0
        if self.sub_name == "add new subject":
            executecommand=ExecuteCommand("modify", {"name":self.stu_name, 'scores_dict':{self.newsub_name:self.score_name}})
            executecommand.return_sig.connect(self.after_send)
            executecommand.run()
        else:
            executecommand=ExecuteCommand("modify", {"name":self.stu_name, 'scores_dict':{self.sub_name:self.score_name}})
            executecommand.return_sig.connect(self.after_send)
            executecommand.run()
    
    def after_send(self,response):
        response = json.loads(response)
        response =  response.get("status", "")
        if response == "OK":
            self.load()
        self.content_label_response.setText(f"The student: {self.stu_name} information sended.", )
