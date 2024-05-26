from PyQt6 import QtWidgets, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent
from client.ServiceController import ExecuteCommand
from WorkWidgets.ShowAllWidget import ShowAllWidget


class DeleteStuWidget(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()

    def __init__(self, name):
        super().__init__()

        self.scores_dict = dict()
        self.name = name

        self.setObjectName("delete_stu_widget")
        self.setWindowTitle("Warning")
        self.setFixedSize(300, 200)

        layout = QtWidgets.QGridLayout()

        self.confirm_button = ButtonComponent("CONFIRM")
        self.confirm_button.clicked.connect(self.confirm_button_pressed)
        self.confirm_button.setEnabled(True)
        layout.addWidget(self.confirm_button, 2, 0, 1, 1)

        self.cancel_button = ButtonComponent("CANCEL")
        self.cancel_button.clicked.connect(self.cancel_button_pressed)
        self.cancel_button.setEnabled(True)
        layout.addWidget(self.cancel_button, 2, 2, 1, 1)

        content = "Are you sure you want to delete?"
        content_label_warning = LabelComponent(16, content=content, 
                                            alignment="center", bg_color=None, 
                                            font_color="red", border_color="lightgray")
        layout.addWidget(content_label_warning, 0, 0, 2, 3)
        # Set Layouts
        for i in range(3):
            layout.setColumnStretch(i, 1)
        for i in range(3):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

    def confirm_button_pressed(self):
        delete_data = {"name": self.name}
        self.execute_delete = ExecuteCommand(command="del", data=delete_data)
        self.execute_delete.start()
        # self.execute_delete.return_sig.connect(self.delete_action_result)
        self.window_closed.emit()
        self.close()

    def cancel_button_pressed(self):
        self.close()
