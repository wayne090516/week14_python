from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget

class AnimatedDialog(QDialog):
    def __init__(self, start_geometry, end_geometry, func_name):
        super().__init__()
        self.setWindowTitle(f"{func_name.capitalize()} Student")
        self.setFixedSize(500, 350)  
        self.start_geometry = start_geometry
        self.end_geometry = end_geometry
        self.func_name = func_name

        oImage = QPixmap("./background/paper.jpg")
        sImage = oImage.scaled(QSize(500,350))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        if func_name == "add":
            self.edit_widget = AddStuWidget()
        elif func_name == "modify":
            self.edit_widget = ModifyStuWidget()
            self.edit_widget.load()
        elif func_name == "del":
            self.edit_widget = DelStuWidget()
            self.edit_widget.load()
        elif func_name == "show":
            self.edit_widget = ShowStuWidget()
            self.edit_widget.load()
    
        self.label = LabelComponent(24, f"{func_name.capitalize()} Student")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit_widget)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close_with_animation)
        layout.addWidget(self.close_button)

        self.selected_name = None
        self.setLayout(layout)
        self.init_open_animation()

    def init_open_animation(self):
        self.open_animation = QPropertyAnimation(self, b"geometry")
        self.open_animation.setDuration(500)
        self.open_animation.setStartValue(self.start_geometry)
        self.open_animation.setEndValue(self.end_geometry)
        self.open_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.open_animation.start()

    def close_with_animation(self):
        self.close_animation = QPropertyAnimation(self, b"geometry")
        self.close_animation.setDuration(500)
        self.close_animation.setStartValue(self.geometry())
        self.close_animation.setEndValue(self.start_geometry)
        self.close_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.close_animation.finished.connect(self.close)
        self.close_animation.start()   

class AddStuAnimatedDialog(AnimatedDialog):
    def __init__(self, start_geometry, end_geometry):
        print("add student")  
        super().__init__(start_geometry, end_geometry, "add")


class ModifyStuAnimatedDialog(AnimatedDialog):
    def __init__(self, start_geometry, end_geometry):
        print("modify student")   
        super().__init__(start_geometry, end_geometry, "modify")

class DelStuAnimatedDialog(AnimatedDialog):
    def __init__(self, start_geometry, end_geometry):
        print("delet student")
        super().__init__(start_geometry, end_geometry, "del")

class ShowAllAnimatedDialog(AnimatedDialog):
    def __init__(self, start_geometry, end_geometry):
        print("show all")
        super().__init__(start_geometry, end_geometry, "show")


