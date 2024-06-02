from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QDialog, QWidget, QGridLayout
from PyQt6.QtCore import QPropertyAnimation, QRect, QSize
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.WidgetComponents import AnimatedLabel
from WorkWidgets.AnimateWidget import AddStuAnimatedDialog, ModifyStuAnimatedDialog, DelStuAnimatedDialog, ShowAllAnimatedDialog


class MainWidget(QWidget):
    def __init__(self, socketclient):
        super().__init__()
        self.setObjectName("main_widget")

        oImage = QPixmap("./background/images.jpg")
        sImage = oImage.scaled(QSize(700,350))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)        

        #title
        layout = QGridLayout()
        self.title = AnimatedLabel("Welcome to student editor!")
        self.title_animation = QPropertyAnimation(self.title, b"opacity")
        self.title_animation.setDuration(2000)
        self.title_animation.setStartValue(0.0)
        self.title_animation.setEndValue(1.0)
        self.title_animation.start()

        #button
        self.add_button = ButtonComponent("Add student")
        self.modify_button = ButtonComponent("Modify student")
        self.del_button = ButtonComponent("Delete student")
        self.show_button = ButtonComponent("Show all")
        self.add_button.setFixedSize(160, 80)
        self.modify_button.setFixedSize(160, 80)
        self.del_button.setFixedSize(160, 80)
        self.show_button.setFixedSize(160, 80)

        #clicked
        self.add_button.clicked.connect(lambda: self.popup("add", self.add_button))
        self.modify_button.clicked.connect(lambda: self.popup("modify", self.modify_button))
        self.del_button.clicked.connect(lambda: self.popup("del", self.del_button))
        self.show_button.clicked.connect(lambda: self.popup("show", self.show_button))

        layout.addWidget(self.title, 0, 0, 1, 4)
        layout.addWidget(self.add_button, 1, 1, 1, 1)
        layout.addWidget(self.modify_button, 1, 2, 1, 1)
        layout.addWidget(self.del_button, 2, 1, 1, 1)
        layout.addWidget(self.show_button, 2, 2, 1, 1)

        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 6)
        layout.setColumnStretch(3, 6)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 3)
        layout.setRowStretch(2, 3)

        self.setLayout(layout)   
    
    def popup(self, func_name, button):
        if hasattr(self, 'dialog') and isinstance(self.dialog, QDialog):
            self.dialog.close()    

        dialog_width = 500  # 對話框的寬度
        dialog_height = 350  # 對話框的高度
        start_x = dialog_width + 250
        start_y = dialog_height + 300
        start_geometry = QRect(int(start_x), int(start_y), dialog_width, dialog_height) # 計算對話框的起始位置，使其位於按鈕上方
        end_geometry = QRect(710, 345, dialog_width, dialog_height) # 設置對話框的結束位置

        if func_name == "add":
            self.dialog = AddStuAnimatedDialog(start_geometry, end_geometry)
        elif func_name == "modify":
            self.dialog = ModifyStuAnimatedDialog(start_geometry, end_geometry)
        elif func_name == "del":
            self.dialog = DelStuAnimatedDialog(start_geometry, end_geometry)
        elif func_name == "show":
            self.dialog = ShowAllAnimatedDialog(start_geometry, end_geometry)
        self.dialog.show() 


       







