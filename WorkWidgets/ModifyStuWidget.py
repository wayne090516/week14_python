from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QFont, QIntValidator
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import json
from client.ServiceCtrl import ServiceCtrl

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        layout = QtWidgets.QGridLayout()
        self.service_ctrl = ServiceCtrl()
        self.scores = {}
        font = QFont("MS UI Gothic", 16) 
        

        header_label = LabelComponent(20, "Modify Student")
        next_step = LabelComponent(16, "\nNext step")
        label_name = LabelComponent(16, "Name：")
        label_subject = LabelComponent(16, "Subject：")

        self.subject_combo_box = QtWidgets.QComboBox(self)
        self.subject_combo_box.setFont(font)
        self.editor_label_subject = LineEditComponent("")
        
        label_score = LabelComponent(16, "Score：")
        self.editor_label_score = LineEditComponent("")
        validator = QIntValidator(0, 999, self)
        self.editor_label_score.setValidator(validator)
        
        self.editor_label_name = QtWidgets.QComboBox()
        self.editor_label_name.setFont(font)
        self.editor_label_name.currentIndexChanged.connect(self.get_subjects)

        self.service_ctrl.show_signal.connect(self.get_name)
        self.service_ctrl.start()   
        self.service_ctrl.show()

        #self.editor_label_name.currentIndexChanged.connect(self.check_conditions)

        self.rb_add = QtWidgets.QRadioButton(self)
        self.rb_add.setText('Add')
        self.rb_add.setFont(font)

        self.rb_modify = QtWidgets.QRadioButton(self)
        self.rb_modify.setText('Modify')
        self.rb_modify.setFont(font)

        self.rb_add.toggled.connect(self.rb_toggled)
        self.rb_modify.toggled.connect(self.rb_toggled)

        # send
        self.button_send = ButtonComponent("send")
        self.button_send.clicked.connect(self.send_act)
        self.message_label = LabelComponent(16, "")  # msg 

        self.editor_label_name.currentTextChanged.connect(self.update_progress)
        self.editor_label_subject.textChanged.connect(self.update_progress)
        self.subject_combo_box.currentTextChanged.connect(self.update_progress)
        self.editor_label_score.textChanged.connect(self.update_progress)
        self.rb_add.toggled.connect(self.update_progress)
        self.rb_modify.toggled.connect(self.update_progress)

        # progress_bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(4)
        self.progress_bar.setValue(0)
        

        # layout
        layout.addWidget(header_label, 0, 0, 1, 2)  # header
        layout.addWidget(self.rb_add, 2, 1, 1, 1)
        layout.addWidget(self.rb_modify, 2, 2, 1, 1)
        layout.addWidget(label_name, 1, 0, 1, 1)
        layout.addWidget(label_subject, 3, 0, 1, 1)

        layout.addWidget(label_score, 4, 0, 1, 1)
        layout.addWidget(self.editor_label_score, 4, 1, 1, 1)
        layout.addWidget(self.editor_label_name, 1, 1, 1, 2)
        layout.addWidget(self.editor_label_subject, 3, 1, 1, 2)
        layout.addWidget(self.subject_combo_box, 3, 1, 1, 2)

        # button
        layout.addWidget(self.button_send, 6, 3, 1, 1)
        layout.addWidget(self.message_label, 5, 2, 1, 2)
        layout.addWidget(next_step, 5, 1, 1, 1)
        layout.addWidget(self.progress_bar, 7, 0, 1, 4)
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
        self.editor_label_score.setText("")
        self.editor_label_subject.setText("")
        self.editor_label_name.setEnabled(1)
        self.button_send.setEnabled(1)
        self.progress_bar.setValue(1)
        self.rb_add.setChecked(True)
        self.message_label.setText("\nInput a subject and score.")
        print("modify widget")

    def showEvent(self, event):
        self.editor_label_name.clear()
        self.service_ctrl.show_signal.connect(self.get_name)
        self.service_ctrl.start()   
        self.service_ctrl.show()

    def get_name(self, response):
        students = response['parameters']
        self.service_ctrl.show_signal.disconnect(self.get_name)
        for student_name in students.keys():
            self.editor_label_name.addItem(student_name)
        self.scores = response['parameters']

    def send_act(self): 
        student_name = self.editor_label_name.currentText().strip()
        existing_subjects = self.get_subjects_for_student(student_name)

        if self.rb_add.isChecked():
            subject = self.editor_label_subject.text().strip()
            if subject in existing_subjects:
                QMessageBox.warning(self, 'Duplicate Subject', 'This subject already exists in the database for the selected student.')
                self.clear_fields() 
                return
        else:
            subject = self.subject_combo_box.currentText().strip()

        score = self.editor_label_score.text().strip()

        if student_name and subject and score:
            try:
                score_value = float(score)
                command = 'modify'
                parameters = {'name': student_name, 'subject': subject, 'score': score_value}
                    
                self.service_ctrl.send(command, parameters)
                QMessageBox.information(self, "Send Information", f"Student {student_name}'s score for {subject} has been handled with {command} command.")
                self.progress_bar.setValue(0)

            except ValueError:
                QMessageBox.warning(self, "Value Error", "Please enter a valid number for the score.")
        else:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields before sending.")
        self.load()
            
    def rb_toggled(self):        
        if self.rb_modify.isChecked():
            self.editor_label_subject.hide()
            self.subject_combo_box.show()
            self.message_label.setText("\nChoose a subject and input score.")
            
        elif self.rb_add.isChecked():
            self.subject_combo_box.hide()
            self.editor_label_subject.show()
            self.message_label.setText("\nInput a subject and score.")

    def get_subjects_for_student(self, student_name):
        # Get subjects for the current student.
        student_info = self.scores.get(student_name, {})
        student_subjects = [score['subject'] for score in student_info.get('scores', [])]
        return student_subjects

    def get_subjects(self, index):
        current_student_name = self.editor_label_name.itemText(index)
        student_subjects = self.get_subjects_for_student(current_student_name)

        # Update the combo box with the current student's subjects.
        self.subject_combo_box.clear()
        self.subject_combo_box.addItems(student_subjects)

    def clear_fields(self):
        if self.rb_modify.isChecked():
            self.editor_label_subject.setText('') 

        if self.rb_add.isChecked():
            self.subject_combo_box.setCurrentIndex(-1) 

    def update_progress(self):
        progress = 0
        if self.editor_label_name.currentText().strip():
            progress += 1
        if self.rb_add.isChecked() and self.editor_label_subject.text().strip():
            progress += 1
        elif self.rb_modify.isChecked() and self.subject_combo_box.currentText().strip():
            progress += 1
        if self.editor_label_score.text().strip():
            progress += 1
        if self.rb_add.isChecked() or self.rb_modify.isChecked():
            progress += 1

        self.progress_bar.setValue(progress)
