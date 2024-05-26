from PyQt6 import QtWidgets, QtCore
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DeleteStuWidget import DeleteStuWidget


class MenuWidget(QtWidgets.QWidget):
    add_student_closed = QtCore.pyqtSignal()
    modify_student_closed = QtCore.pyqtSignal()
    delete_student_closed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("menu_widget")

        layout = QtWidgets.QGridLayout()
        self.add_stu_button = ButtonComponent("Add student")
        self.modify_stu_button = ButtonComponent("Modify student")
        self.delete_stu_button = ButtonComponent("Delete student")

        self.add_stu_button.setEnabled(True)
        self.modify_stu_button.setEnabled(True)
        self.delete_stu_button.setEnabled(False)

        self.add_stu_button.clicked.connect(self.add_student_popup)
        self.modify_stu_button.clicked.connect(self.modify_student_popup)
        self.delete_stu_button.clicked.connect(self.delete_student_popup)

        layout.addWidget(self.add_stu_button, 0, 0)
        layout.addWidget(self.modify_stu_button, 1, 0)
        layout.addWidget(self.delete_stu_button, 2, 0)

        for i in range(3):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)
        self.selected_name = None

    def add_student_popup(self):
        self.add_stu_popup = AddStuWidget()
        self.add_stu_popup.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.add_stu_popup.window_closed.connect(self.add_student_closed.emit)
        self.add_stu_popup.show()

    def modify_student_popup(self):
        self.modify_stu_popup = ModifyStuWidget()
        self.modify_stu_popup.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.modify_stu_popup.window_closed.connect(self.modify_student_closed.emit)
        self.modify_stu_popup.show()

    def delete_student_popup(self):
        self.delete_stu_popup = DeleteStuWidget(self.selected_name)
        self.delete_stu_popup.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.delete_stu_popup.window_closed.connect(self.delete_student_closed.emit)
        self.delete_stu_popup.show()
    
    def handle_name_clicked(self, name):
        self.selected_name = name
        self.delete_stu_button.setEnabled(True)