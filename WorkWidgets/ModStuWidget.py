from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from socket_cli.Control import ExecuteCommand
from socket_cli.Socket_cli import SocketClient

class ModStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("mod_stu_widget")

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Modify Scores")
        content_label_name = LabelComponent(16, "Name: ")
        self.combobox_name = ComboBoxComponent()
        self.combobox_name.currentTextChanged.connect(self.name_change)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(content_label_name, 1, 0, 1, 1)
        layout.addWidget(self.combobox_name, 1, 1, 1, 1)

        content_label_subject = LabelComponent(16, "Subject: ")
        self.combobox_subject = ComboBoxComponent()
        self.combobox_subject.currentTextChanged.connect(self.subject_change)

        layout.addWidget(content_label_subject, 2, 0, 1, 1)
        layout.addWidget(self.combobox_subject, 2, 1, 1, 1)

        self.editor_label_newsubject = LineEditComponent("Subject")
        self.editor_label_newsubject.disable()

        layout.addWidget(self.editor_label_newsubject, 3, 1, 1, 1)

        content_label_score = LabelComponent(16, "Score: ")
        self.editor_label_score = LineEditComponent()
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.setValidator(QtGui.QIntValidator())
        
        layout.addWidget(content_label_score, 4, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 4, 1, 1, 1)

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

    def load(self):
        self.combobox_name.clear()
        self.combobox_subject.clear()
        self.editor_label_newsubject.disable()
        self.editor_label_score.setText("")
        executecommand=ExecuteCommand(self.client, "show", "")
        executecommand.return_sig.connect(self.get_dict)
        executecommand.run()
   
    def get_dict(self,received_data):
        student_dict=eval(received_data)
        self.student_dict=student_dict["parameters"]
        for key in self.student_dict:
            self.combobox_name.addItem(key)

    def name_change(self):
        if self.combobox_name.currentText() !="":
            self.combobox_subject.clear()
            self.editor_label_score.setText("")
            self.editor_label_newsubject.setText("Subject")
            score_dict=self.student_dict[self.combobox_name.currentText()]
            self.combobox_subject.addItem("add new score")
            for key in score_dict:
                self.combobox_subject.addItem(key)
            self.editor_label_newsubject.enable()
            
    def subject_change(self):
        if self.combobox_subject.currentText() !="add new score":
            self.editor_label_newsubject.disable()
        else:
            self.editor_label_newsubject.enable()


    def send(self):
        if self.combobox_name.currentText()=="" or self.editor_label_score.text() =="" or (self.combobox_name.currentText()=="add new score" and self.editor_label_newsubject.text==""):
            self.content_label_respon.setText("Please enter information.")
            return 0
        if self.combobox_name.currentText() =="add new score":
            executecommand=ExecuteCommand(self.client, "modify", {"name":self.combobox_name.currentText(), 'scores':{self.editor_label_newsubject.text():self.editor_label_score.text()}})
            executecommand.return_sig.connect(self.after_send)
            executecommand.run()
        else:
            executecommand=ExecuteCommand(self.client, "modify", {"name":self.combobox_name.currentText(), 'scores_dict':{self.combobox_subject.currentText():self.editor_label_score.text()}})
            executecommand.return_sig.connect(self.after_send)
            executecommand.run()
    
    def after_send(self,response):
        response=eval(response)
        if response["status"]=="OK":
            self.load()
        self.content_label_respon.setText("The information: <br>"+str(response["reason"]))

