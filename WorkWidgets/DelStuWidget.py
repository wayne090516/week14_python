from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtMultimedia import QSoundEffect
from WorkWidgets.WidgetComponents import ButtonComponent, ComboBoxComponent, ScrollComponent
from client.ServiceControl import ExecuteCommand
from client.SocketClient import SocketClient
import json
import os

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Del_stu_widget")

        layout = QtWidgets.QGridLayout()
        self.scrollable_label = ScrollComponent(12, "")

        self.name_combobox = ComboBoxComponent()
        self.sub_combobox = ComboBoxComponent()

        self.del_button = ButtonComponent("delete")
        self.del_button.clicked.connect(self.del_stu)

        self.sound_effect = QSoundEffect()
        sound_effect_path = os.path.abspath("./sound/sound_effect.wav")  # 替换为你的音效文件路径
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_effect_path))


        layout.addWidget(self.scrollable_label, 0, 0, 1, 2)
        layout.addWidget(self.name_combobox, 1, 0, 1, 2)
        layout.addWidget(self.del_button, 2, 0, 1, 2)


        layout.setColumnStretch(0, 5)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 5)
        layout.setRowStretch(2, 1)
        
        self.setLayout(layout)
        self.client = SocketClient()

    def load(self):
        self.name_combobox.clear()
        executecommand = ExecuteCommand("show", {})
        executecommand.return_sig.connect(self.printall)
        executecommand.run()

    def del_stu(self):
        if self.name_combobox.currentText() != "":
            reply = QMessageBox.question(self, 'Delete Confirmation', 
                                        'Did you really want to delete?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.play_sound_effect()
                executecommand = ExecuteCommand("del", {"name": self.name_combobox.currentText()})
                executecommand.return_sig.connect(self.load)
                executecommand.run()
                
    def play_sound_effect(self):
        self.sound_effect.play()

    def printall(self, received_data):
        self.student_dict = json.loads(received_data)
        self.student_dict = self.student_dict.get("parameters", {})
        for name in self.student_dict:
            self.name_combobox.addItem(name)  # 将学生姓名添加到combobox中
        stu = "\n==== student list ====\n"
        for name, scores in self.student_dict.items():
            stu += (f"Name: {name}\n")
            for subject, score in scores.items():
                stu += (f"  subject: {subject}, scores: {score}\n")
            stu += ("\n")
        stu += "======================"
        print(stu)
        self.scrollable_label.set_text(stu)  
 
        

