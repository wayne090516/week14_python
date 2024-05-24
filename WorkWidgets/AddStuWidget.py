from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from socket_cli.Control import ExecuteCommand
from socket_cli.Socket_cli import SocketClient

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        content_label_name = LabelComponent(16, "Name: ")
        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_change)
        self.button_query = ButtonComponent("Query")
        self.button_query.clicked.connect(self.query)
        self.button_query.disable()

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(content_label_name, 1, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 1, 1, 1, 1)
        layout.addWidget(self.button_query, 1, 2, 1, 1)

        content_label_subject = LabelComponent(16, "Subject: ")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_subject.disable()

        layout.addWidget(content_label_subject, 2, 0, 1, 1)
        layout.addWidget(self.editor_label_subject, 2, 1, 1, 1)

        content_label_score = LabelComponent(16, "Score: ")
        self.editor_label_score = LineEditComponent()
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.disable()
        self.editor_label_score.setValidator(QtGui.QIntValidator())
        self.editor_label_score.textChanged.connect(self.score_change)
        self.button_add = ButtonComponent("Add")
        self.button_add.clicked.connect(self.add)
        self.button_add.disable()
        
        layout.addWidget(content_label_score, 3, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 1)
        layout.addWidget(self.button_add, 3, 2, 1, 1)

        self.content_label_respon = LabelComponent(16, "", "color:red;")
        self.button_send = ButtonComponent("Send")
        self.button_send.clicked.connect(self.send)

        layout.addWidget(self.content_label_respon, 0, 4, 5, 1)
        layout.addWidget(self.button_send, 6, 4, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 4)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 2)
        layout.setRowStretch(5, 2)
        layout.setRowStretch(6, 2)
        self.setLayout(layout)

        self.client = SocketClient()
        self.score_dict=dict()

   
    def name_change(self):
        if self.editor_label_name.text() !="":
            self.button_query.enable()
        
    
    def score_change(self):
        if self.editor_label_score.text() !="":
            self.button_add.enable()    


    def query(self):
        print("Name :" +self.editor_label_name.text())
        executecommand=ExecuteCommand(self.client, "query", {"name":self.editor_label_name.text()})
        executecommand.return_sig.connect(self.after_query)
        executecommand.run()

    def after_query(self,response):
        response=eval(response)
        if response["status"]=="Fail":
            self.editor_label_name.disable()
            self.editor_label_subject.enable()
            self.editor_label_score.enable()
            self.button_send.disable()
        else:
            self.content_label_respon.setText("The information: <br>"+response["reason"])
        


    def add(self):
        if (self.editor_label_name.text() ==""or self.editor_label_subject.text() =="" or self.editor_label_score.text() ==""):
            self.content_label_respon.setText("Please enter the score data")
        else:
            self.score_dict[self.editor_label_subject.text()]=self.editor_label_score.text()
            self.button_send.enable()
            self.content_label_respon.setText("The information: <br>"+str({'status': "OK", 'reason': (f"add {self.editor_label_subject.text()} : {self.editor_label_score.text()}")}))


    def send(self, response):
        executecommand=ExecuteCommand(self.client, "add", {"name":self.editor_label_name.text(), 'scores':self.score_dict})
        executecommand.return_sig.connect(self.after_send)
        executecommand.run()
    
    def after_send(self,response):
        response=eval(response)
        if response["status"]=="OK":
            self.editor_label_name.enable()
            self.editor_label_name.setText("Name")
            self.editor_label_subject.setText("Subject")
            self.editor_label_score.setText("")
            self.editor_label_subject.disable()
            self.editor_label_score.disable()
            self.button_query.disable()
            self.button_add.disable()
            self.button_send.disable()
            self.score_dict=dict()
        self.content_label_respon.setText("The information: <br>"+str(response["reason"]))
        self.score_dict=dict()

    def load(self):
        print("add widget")
        self.editor_label_name.enable()
        self.editor_label_name.setText("Name")
        self.editor_label_subject.setText("Subject")
        self.editor_label_score.setText("")
        self.editor_label_subject.disable()
        self.editor_label_score.disable()
        self.button_query.disable()
        self.button_add.disable()
        self.button_send.disable()
        self.score_dict=dict()
        self.content_label_respon.setText("")

