from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent
from client.ServiceController import ExecuteCommand

class DeleteStuWidget(QtWidgets.QWidget):
    window_closed = QtCore.pyqtSignal()

    def __init__(self, name):
        super().__init__()

        self.scores_dict = dict()
        self.name = name

        window_length = 300
        window_width = 100

        self.setObjectName("delete_stu_widget")
        self.setWindowTitle("Warning")
        self.setFixedSize(window_length, window_width)

        oImage = QPixmap("./WorkWidgets/images/background_2.jpg")
        sImage = oImage.scaled(QSize(window_length, window_width))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        layout = QtWidgets.QGridLayout()

        self.confirm_button = ButtonComponent(16, content="CONFIRM", 
                                              style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #FF8000}
                                                        ButtonComponent:hover {background-color: #606060;}''')
        self.confirm_button.clicked.connect(self.confirm_button_pressed)
        self.confirm_button.setEnabled(True)
        layout.addWidget(self.confirm_button, 2, 0, 1, 1)

        self.cancel_button = ButtonComponent(16, content="CANCEL",
                                             style='''ButtonComponent{background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #808080, stop:1 #404040); border-radius: 5px; color: #00cc00}
                                                        ButtonComponent:hover {background-color: #606060;}''')
        self.cancel_button.clicked.connect(self.cancel_button_pressed)
        self.cancel_button.setEnabled(True)
        layout.addWidget(self.cancel_button, 2, 2, 1, 1)

        content = "Are you sure you want to delete?"
        content_label_warning = LabelComponent(12, content=content, alignment="center", 
                                               style=f"background-color: {None}; color: red;")
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
        self.window_closed.emit()
        self.close()

    def cancel_button_pressed(self):
        self.close()
