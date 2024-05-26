from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QFont
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import json
from client.ServiceCtrl import ServiceCtrl

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("del_stu_widget")
        layout = QtWidgets.QGridLayout()
        self.service_ctrl = ServiceCtrl()
        self.scores = {}
        header_label = LabelComponent(20, "Delete Student")
        next_step = LabelComponent(16, "Next step")

        font = QFont("MS UI Gothic", 16) 
        self.editor_label_del = QtWidgets.QComboBox()
        self.editor_label_del.setFont(font)

        self.check_box = QtWidgets.QCheckBox("Confirm deletion")
        self.check_box.setFont(font)

        self.service_ctrl.show_signal.connect(self.get_name)
        self.service_ctrl.start()   
        self.service_ctrl.show()

        self.editor_label_del.currentIndexChanged.connect(self.check_conditions)
        self.check_box.stateChanged.connect(self.check_conditions)

        # send
        self.button_send = ButtonComponent("send")
        self.button_send.clicked.connect(self.send_act)
        self.message_label = LabelComponent(16, "")  # msg 

        # progress_bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(2)
        self.progress_bar.setValue(0)
        
        # layout
        layout.addWidget(header_label, 0, 0, 1, 2)  # header
        layout.addWidget(self.check_box, 3, 0, 1, 2)
        layout.addWidget(self.editor_label_del, 2, 0, 1, 2)
                
        # button
        layout.addWidget(self.button_send, 6, 3, 1, 1)
        layout.addWidget(self.message_label, 5, 2, 1, 3)
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
        self.editor_label_del.setEnabled(1)
        self.button_send.setEnabled(0)
        self.check_box.setEnabled(1)
        self.progress_bar.setValue(1)
        self.message_label.setText("Choose a student & confirm.")
        print("del widget")

    def showEvent(self, event):
        self.editor_label_del.clear()  # 清除所有的學生名字 
        self.service_ctrl.show_signal.connect(self.get_name)
        self.service_ctrl.start()   
        self.service_ctrl.show()

    def get_name(self, response):
        students = response['parameters']
        self.service_ctrl.show_signal.disconnect(self.get_name)  # 斷開連接以避免重複添加名字
        for student_name in students.keys():
            self.editor_label_del.addItem(student_name)

    def send_act(self): 
        student_name = self.editor_label_del.currentText()
        self.service_ctrl.send("del", {'name': student_name})
        self.editor_label_del.removeItem(self.editor_label_del.currentIndex())
        self.progress_bar.setValue(0)
        self.check_box.setChecked(False)
        #self.message_label.setText(f"Student {student_name} has been deleted.")
        QMessageBox.information(self, "Send information", f"Student {student_name} has been deleted.")
            

    def check_conditions(self):
        student_name = self.editor_label_del.currentText()
        checkbox_checked = self.check_box.isChecked()
        if student_name and not checkbox_checked:
            self.progress_bar.setValue(1)
        elif student_name and checkbox_checked:
            self.progress_bar.setValue(2)
            self.button_send.setEnabled(True)
        else:
            self.button_send.setEnabled(False)
