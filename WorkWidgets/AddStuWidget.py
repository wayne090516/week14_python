from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import json
from client.ServiceCtrl import ServiceCtrl

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")
        layout = QtWidgets.QGridLayout()
        self.scores = {}
        header_label = LabelComponent(20, "Add  Student")
        self.service_ctrl = ServiceCtrl()
        next_step = LabelComponent(16, "Next step")
        # ------label & editor-----------------------------------------------------
        # name
        name_label = LabelComponent(16, "Name: ")
        self.editor_label_name = LineEditComponent("Name")
        self.editor_label_name.mousePressEvent = self.clear_editor_name
        self.editor_label_name.textChanged.connect(self.name_change)
        # subject
        subject_label = LabelComponent(16, "Subject: ")
        self.editor_label_subject = LineEditComponent("Subject")
        self.editor_label_subject.mousePressEvent = self.clear_editor_subject
        self.editor_label_subject.textChanged.connect(self.subject_text_change)
        self.subject_progress_added = False
        # score
        score_label = LabelComponent(16, "Score: ")
        self.editor_label_score = LineEditComponent("")
        self.editor_label_score.setValidator(QtGui.QIntValidator(0, 100))
        self.editor_label_score.mousePressEvent = self.clear_editor_score       
        self.score_progress_added = False
        
        self.editor_label_score.textChanged.connect(self.check_empty)
        self.editor_label_score.textChanged.connect(self.score_text_change)

        self.editor_label_subject.textChanged.connect(self.check_empty)
        self.editor_label_score.textChanged.connect(self.check_empty)
        self.editor_label_name.textChanged.connect(self.check_empty)

        # ------button-------------------------------------------------------------
        # query
        self.button_query = ButtonComponent("query")
        self.button_query.clicked.connect(self.query_act)
        self.query_pressed = False
        # add
        self.button_add = ButtonComponent("add")
        self.button_add.clicked.connect(self.add_act)
        self.add_pressed = False
        # send
        self.button_send = ButtonComponent("send")
        self.button_send.clicked.connect(self.send_act)
        self.message_label = LabelComponent(16, "")  # msg 
        # ------progress_bar-------------------------------------------------------
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(3)
        self.progress_bar.setValue(0)
        
        # ------layout-------------------------------------------------------------
        layout.addWidget(header_label, 0, 0, 1, 2)  # header
        # label
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        # editor
        layout.addWidget(self.editor_label_name, 1, 1, 1, 1)
        layout.addWidget(self.editor_label_subject, 2, 1, 1, 1)
        layout.addWidget(self.editor_label_score, 3, 1, 1, 1)
        # button
        layout.addWidget(self.button_query, 1, 2, 1, 1)
        layout.addWidget(self.button_add, 3, 2, 1, 1)
        layout.addWidget(self.button_send, 6, 3, 1, 1)
        layout.addWidget(self.message_label, 5, 2, 1, 3)
        layout.addWidget(next_step, 5, 1, 1, 1)
        layout.addWidget(self.progress_bar, 7, 0, 1, 4)  # or any other position you prefer
        # ------row & column-------------------------------------------------------
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 4)
        layout.setColumnStretch(3, 4)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 3)
        layout.setRowStretch(5, 3)
        layout.setRowStretch(6, 5)
        layout.setRowStretch(7, 1)

        self.setLayout(layout)
        self.load()

    def load(self):
        self.editor_label_name.setText("Name")
        self.editor_label_name.setEnabled(True)
        self.editor_label_subject.setText("Subject")
        self.editor_label_subject.setEnabled(False)
        self.editor_label_score.setText("")
        self.editor_label_score.setEnabled(False)
        self.button_query.setEnabled(False)
        self.button_add.setEnabled(False)
        self.button_send.setEnabled(False)
        self.progress_bar.setValue(0)
        self.message_label.setText("Input student's name")
        self.scores = {}
        print("add widget")

    def name_change(self, text):
        if text.strip() and self.progress_bar.value() == 0:  
            self.progress_bar.setValue(self.progress_bar.value() + 1)
        self.button_query.setEnabled(bool(text))

    def clear_editor_name(self, event):  
        self.progress_bar.setValue(0)
        self.editor_label_name.clear()

    def subject_text_change(self, text):
        # Only add progress the first time characters are entered
        if text.strip() and not self.subject_progress_added:
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.subject_progress_added = True

    def clear_editor_subject(self, event):
        self.editor_label_subject.clear()
        # Reset progress bar status for subject input box
        self.subject_progress_added = False
        
    def score_text_change(self, text):
        # Only add progress the first time characters are entered
        if text.strip() and not self.score_progress_added:
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.score_progress_added = True

    def clear_editor_score(self, event):
        self.editor_label_score.clear()
        # Reset progress bar status for score input box
        self.score_progress_added = False
        
    def check_empty(self):
        if self.editor_label_subject.text().strip() and self.editor_label_score.text().strip():
            self.message_label.setText("Press add.")
        elif not self.query_pressed and self.editor_label_name.text().strip():
            self.message_label.setText("Press query.")

    def query_act(self):
        if self.editor_label_name.text():
            name = self.editor_label_name.text()
            response = self.service_ctrl.query(name)
            if response.get('status') == 'failed':
                #self.message_label.setText(f"{name} does not exist.")
                QMessageBox.information(self, "Query information", f"{name} does not exist.")
                self.editor_label_name.setEnabled(False)
                self.button_add.setEnabled(True)
                self.editor_label_subject.setEnabled(True)
                self.editor_label_score.setEnabled(True)
                self.message_label.setText("Input student's subject & score")
                self.query_pressed = True
            else:
                #self.message_label.setText(f"{name} does exist")
                QMessageBox.information(self, "Query information", f"{name} does exist.\nPlease input another name.")

    def add_act(self):
        if not self.editor_label_name.text().strip() or not self.editor_label_subject.text().strip() or not self.editor_label_score.text().strip():
            #self.message_label.setText("Name, Subject and Score cannot be empty.")
            QMessageBox.information(self, "Add information", f"Name, Subject and Score cannot be empty.")
        else:
            name = self.editor_label_name.text()
            subject = self.editor_label_subject.text()
            score = self.editor_label_score.text()

            if name not in self.scores:
                self.scores[name] = {}

            if subject in self.scores[name]:
                #self.message_label.setText(f"The subject {subject} is already in the records for student {name}.")
                QMessageBox.information(self, "Add information", f"The subject {subject} is already in the records for student {name}.")
            else:
                self.scores[name][subject] = score                
                #self.message_label.setText(f"Name: {name},\nSubject: {subject},\nScore: {score}")
                QMessageBox.information(self, "Add information", f"Name: {name},\nSubject: {subject},\nScore: {score}")
                self.button_send.setEnabled(True)
                self.add_pressed = True
                self.message_label.setText(f"Keep add or press send.")

    def send_act(self):
        name = self.editor_label_name.text()
        score = self.scores.get(name)
        if score is not None:
            response = self.service_ctrl.send('add', {'name': name, 'scores': self.scores[name]})
            self.scores.pop(name, None)
            QMessageBox.information(self, "Send information", f"Student scores successfully sent.")
            #self.message_label.setText("Student scores successfully sent.")
        else:
            QMessageBox.information(self, "Send information", f"No score to send.")
            #self.message_label.setText("No score to send.")
        self.load()
