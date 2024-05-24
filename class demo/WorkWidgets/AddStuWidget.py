from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent

import time

from PyQt6.QtCore import pyqtSignal
import json


class AddStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("add_stu_widget")

        layout = QtWidgets.QGridLayout()

        header_label = LabelComponent(20, "Add Student")
        content_label = LabelComponent(16, "Name: ")
        self.editor_label = LineEditComponent("Name")
        self.editor_label.mousePressEvent = self.clear_editor_content
        button = ButtonComponent("Confirm")
        button.clicked.connect(self.confirm_action)
        self.message_label = LabelComponent(16, "")

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(content_label, 1, 0, 1, 1)
        layout.addWidget(self.editor_label, 1, 1, 1, 1)
        layout.addWidget(button, 2, 1, 1, 1)
        layout.addWidget(self.message_label, 2, 0, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 9)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 5)

        self.setLayout(layout)

    def load(self):
        print("add widget")

    def clear_editor_content(self, event):
        self.editor_label.clear()

    def confirm_action(self):
        self.send_command = ExecuteConfirmCommand(10)
        self.send_command.start()
        self.send_command.return_sig.connect(self.process_result)

    def process_result(self, result):
        result = json.loads(result)
        self.message_label.setText("count: {}".format(result['message']))

class ExecuteConfirmCommand(QtCore.QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, counts):
        super().__init__()
        self.counts = counts

    def run(self):
        result_dict = dict()
        for i in range(self.counts):
            result_dict['message'] = i
            self.return_sig.emit(json.dumps(result_dict))
            time.sleep(1)
