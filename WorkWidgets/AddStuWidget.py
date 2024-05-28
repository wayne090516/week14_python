from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ScrollLabelComponent
from client.ServiceController import ExecuteCommand
import json


class AddStuWidget(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.scores_dict = dict()

        window_length = 400
        window_width = 200

        self.setObjectName("add_stu_widget")
        self.setWindowTitle("Add Student")
        self.setFixedSize(window_length, window_width)

        oImage = QPixmap("./WorkWidgets/images/background_2.jpg")
        sImage = oImage.scaled(QSize(window_length, window_width))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        layout = QtWidgets.QGridLayout()

        # Name and Query-button
        content_label_name = LabelComponent(16, content="Name:", alignment="right", 
                                            style=f"background: transparent; color: #00cc00;")
        self.editor_label_name = LineEditComponent(16, default_content="Name",alignment="left")
        self.editor_label_name.mousePressEvent = self.editor_label_name.clear_editor_content
        self.editor_label_name.textChanged.connect(self.name_entered)
        layout.addWidget(content_label_name, 0, 0, 1, 1)
        layout.addWidget(self.editor_label_name, 0, 1, 1, 2)

        self.button_query = ButtonComponent(16, content="Check", 
                                            style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #00cc00}
                                                    ButtonComponent:hover {background-color: #606060;}''')
        self.button_query.clicked.connect(self.query_pressed)
        self.button_query.setEnabled(False)
        layout.addWidget(self.button_query, 0, 3, 1, 2)

        # Subject and Add-button
        content_label_subject = LabelComponent(16, content="Subject:", alignment="right", 
                                               style=f"background: transparent; color: #00cc00;")
        self.editor_label_subject = LineEditComponent(16, default_content="Subject",alignment="left")
        self.editor_label_subject.mousePressEvent = self.editor_label_subject.clear_editor_content
        self.editor_label_subject.textChanged.connect(self.subject_blanked)
        self.editor_label_subject.setEnabled(False)
        layout.addWidget(content_label_subject, 1, 0, 1, 1)
        layout.addWidget(self.editor_label_subject, 1, 1, 1, 2)

        self.button_add = ButtonComponent(16, content="Add", 
                                          style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #00cc00}
                                                    ButtonComponent:hover {background-color: #606060;}''')
        self.button_add.clicked.connect(self.add_pressed)
        self.button_add.setEnabled(False)
        layout.addWidget(self.button_add, 1, 3, 1, 2)


        # Score and Send-button
        content_label_score = LabelComponent(16, content="Score:", alignment="right", 
                                             style=f"background: transparent; color: #00cc00;")
        self.editor_label_score = LineEditComponent(16, default_content="Score",alignment="left")
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.setValidator(QtGui.QIntValidator(0, 100)) 
        self.editor_label_score.textChanged.connect(self.score_blanked)
        self.editor_label_score.setEnabled(False)
        layout.addWidget(content_label_score, 2, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 2, 1, 1, 2)

        self.button_send = ButtonComponent(16, content="Send", 
                                           style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #00cc00}
                                                    ButtonComponent:hover {background-color: #606060;}''')
        self.button_send.clicked.connect(self.send_pressed)
        self.button_send.setEnabled(False)
        layout.addWidget(self.button_send, 2, 3, 1, 2)
      
        # Respond-window 
        self.respond_window = LabelComponent(12, content="", alignment="left",
                                             style=f"background: transparent; color: red;")
        layout.addWidget(self.respond_window, 3, 0, 1, 5)
        
        # Set Layouts
        for i in range(5):
            layout.setColumnStretch(i, 1)
        for i in range(4):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

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
            self.respond_window.setText("Please add student's information.")
        elif status == "OK":
            self.editor_label_name.setText("Name")
            self.respond_window.setText("The student already existed!")

    def add_pressed(self):
        if (self.editor_label_name.text()=="" or self.editor_label_subject.text()=="" or self.editor_label_score.text()==""):
            self.respond_window.setText("Please enter the subject and score for the student!")
        else:
            self.button_send.setEnabled(True)
            self.scores_dict[self.editor_label_subject.text()] = self.editor_label_score.text()
            self.parameters = {'name': self.name, 'scores': self.scores_dict}
            self.respond_window.setText(f"{self.parameters} added")

    def send_pressed(self):
        send_data = self.parameters
        self.execute_send = ExecuteCommand(command="add", data=send_data)
        self.execute_send.start()
        self.execute_send.return_sig.connect(self.send_action_result)

    def send_action_result(self, result):
        status = eval(json.loads(result))["status"]

        if status == "Fail":
            self.respond_window.setText("Add " + str(self.parameters) + " failed!")
        elif status == "OK":
            self.load()
            self.respond_window.setText("Add " + str(self.parameters) + " successfully!")

    def name_entered(self):
        if self.editor_label_name.text() != "":
            self.button_query.setEnabled(True)

    def subject_blanked(self):
        if self.editor_label_subject.text() == "":
            self.button_send.setEnabled(False)
    
    def score_blanked(self):
        if self.editor_label_score.text() == "":
            self.button_add.setEnabled(True)
            self.button_send.setEnabled(False)