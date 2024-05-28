from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent
from client.ServiceController import ExecuteCommand
from WorkWidgets.ShowAllWidget import ShowAllWidget
import json

class ModifyStuWidget(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()

    def __init__(self, names_list, subject_dict):
        super().__init__()

        self.names_list = names_list
        self.subject_dict = subject_dict

        window_length = 400
        window_width = 300

        self.setObjectName("modify_stu_widget")
        self.setWindowTitle("Modify Student")
        self.setFixedSize(window_length, window_width)

        oImage = QPixmap("./WorkWidgets/images/background_2.jpg")
        sImage = oImage.scaled(QSize(window_length, window_width))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        layout = QtWidgets.QGridLayout()

        # Name
        content_label_name = LabelComponent(16, content="Name:", alignment="right", 
                                            style=f"background: transparent; color: #00cc00;")
        
        self.combobox_name = ComboBoxComponent()
        self.name_list_parse(self.names_list)
        self.combobox_name.currentTextChanged.connect(self.name_change)

        layout.addWidget(content_label_name, 0, 0, 1, 1)
        layout.addWidget(self.combobox_name, 0, 1, 1, 2)

        # Subject
        content_label_subject = LabelComponent(16, content="Subject:", alignment="right", 
                                               style=f"background: transparent; color: #00cc00;")
        
        self.combobox_subject = ComboBoxComponent()
        self.combobox_subject.currentTextChanged.connect(self.subject_change)

        self.editor_label_newsubject = LineEditComponent(16, default_content="New Subject",alignment="center")
        self.editor_label_newsubject.textChanged.connect(self.newsubject_blanked)
        self.editor_label_newsubject.mousePressEvent = self.editor_label_newsubject.clear_editor_content

        self.combobox_subject.setEnabled(False)
        self.editor_label_newsubject.setEnabled(False)

        layout.addWidget(content_label_subject, 1, 0, 1, 1)
        layout.addWidget(self.combobox_subject, 1, 1, 1, 2)
        layout.addWidget(self.editor_label_newsubject, 2, 1, 1, 2)

        # Score and Send-button
        content_label_score = LabelComponent(16, content="Score:", alignment="right",
                                             style=f"background: transparent; color: #00cc00;")
        self.editor_label_score = LineEditComponent(16, default_content="Score",alignment="center")
        self.editor_label_score.mousePressEvent = self.editor_label_score.clear_editor_content
        self.editor_label_score.setValidator(QtGui.QIntValidator(0, 100))
        self.editor_label_score.textChanged.connect(self.score_blanked)
        self.editor_label_score.setEnabled(False)

        layout.addWidget(content_label_score, 3, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 2)

        self.button_modify = ButtonComponent(16, content="Modify", 
                                           style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #00cc00}
                                                    ButtonComponent:hover {background-color: #606060;}''')
        self.button_modify.clicked.connect(self.modify_pressed)
        self.button_modify.setEnabled(False)

        layout.addWidget(self.button_modify, 4, 0, 1, 3)

        # Respond-window 
        self.respond_window = LabelComponent(16, content="", alignment="left", 
                                             style=f"background: transparent; color: red;")
        
        layout.addWidget(self.respond_window, 5, 0, 1, 3)
        
        # Set Layouts
        for i in range(3):
            layout.setColumnStretch(i, 1)
        for i in range(6):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

    def load(self):
        self.combobox_name.clear()
        self.combobox_subject.clear()
        self.editor_label_newsubject.setText("New Subject")
        self.editor_label_newsubject.setEnabled(False)
        self.editor_label_score.setText("Score")
        self.editor_label_score.setEnabled(False)
        self.show_all_widget = ShowAllWidget()
        self.show_all_widget.get_refreshed_data()
        self.names_list = self.show_all_widget.names
        self.subject_dict = self.show_all_widget.subjects_dict
        self.name_list_parse(self.names_list)

    def modify_pressed(self):
        repeated_flag = False
        if self.combobox_subject.currentText()!="add new score":
            parts = self.combobox_subject.currentText().split(':')
            subject_score = {parts[0]: self.editor_label_score.text()}
        else:
            for subject in self.subjects:
                if self.editor_label_newsubject.text() == str(subject.split(':')[0]) :
                    self.button_modify.setEnabled(False)
                    self.respond_window.setText("The subject already exists, please enter a new subject!")
                    self.editor_label_newsubject.setText("")
                    self.editor_label_score.setText("")
                    repeated_flag = True
                else:
                    subject_score = {self.editor_label_newsubject.text(): self.editor_label_score.text()}
                    self.button_modify.setEnabled(True)

        if not repeated_flag:
            self.send_data = {'name': self.combobox_name.currentText(), 'scores': subject_score}
            self.execute_modify = ExecuteCommand(command="modify", data=self.send_data)
            self.execute_modify.start()
            self.execute_modify.return_sig.connect(self.modify_action_result)

    def modify_action_result(self, result):
        status = eval(json.loads(result))["status"]
        self.load()

        if status == "Fail":
            self.respond_window.setText("Modify " + str(self.send_data) + " failed!")
        elif status == "OK":
            self.respond_window.setText("Modify " + str(self.send_data) + " successfully!")

    def score_blanked(self):
        if self.editor_label_score.text() == "":
            self.button_modify.setEnabled(False)
        else:
            self.button_modify.setEnabled(True)

    def newsubject_blanked(self):
        self.editor_label_score.setText("Score")
        if self.editor_label_newsubject.text() == "":
            self.editor_label_score.setEnabled(False)
        else:
            self.editor_label_score.setEnabled(True)

    def name_list_parse(self, name_list):
        self.combobox_name.addItem("")
        for name in name_list:
            self.combobox_name.addItem(name)

    def name_change(self):
        if self.combobox_name.currentText()!="":
            self.combobox_subject.setEnabled(True)
            self.combobox_subject.clear()
            self.editor_label_score.setText("Score")
            self.editor_label_newsubject.setText("New Subject")
            self.editor_label_newsubject.setEnabled(True)
            self.subjects = self.subject_dict[self.combobox_name.currentText()]
            self.combobox_subject.addItem("add new score")
            for subject in self.subjects:
                self.combobox_subject.addItem(subject)

            
    def subject_change(self):
        if self.combobox_name.currentText()!="":
            self.editor_label_score.setEnabled(True)
            self.editor_label_score.setText("Score")
            self.editor_label_newsubject.setText("New Subject")
            if self.combobox_subject.currentText()!="add new score":
                self.editor_label_newsubject.setEnabled(False)
            else:
                self.editor_label_newsubject.setEnabled(True)
