from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModStuWidget import ModStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import LabelComponent, Mute_label, ButtonComponent
from WorkWidgets.MusicPlayer import MusicPlayer


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(menu_widget, 1, 0, 1, 1)
        layout.addWidget(function_widget, 1, 1, 1, 1)

        self.setLayout(layout)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("src/background_image.jpg")  # 替换为你的城市背景图片路径
        painter.drawPixmap(self.rect(), pixmap)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QVBoxLayout()
        add_button = ButtonComponent("Add")
        del_button = ButtonComponent("Del")
        mod_button = ButtonComponent("Mod")
        show_button = ButtonComponent("Show")
        
        self.musicplayer = MusicPlayer()
        self.musicplayer.play_music("src/music.mp3")
        self.mute_label = Mute_label()
        self.mute_label.set_mute_icon(False)
        self.mute_label.mousePressEvent = self.mute_toggle

        # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        mod_button.clicked.connect(lambda: self.update_widget_callback("mod"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))

        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(mod_button)
        layout.addWidget(show_button)
        layout.addWidget(self.mute_label)

        self.setLayout(layout)


    def mute_toggle(self, a):
        print("mute_toggle")
        self.mute_label.set_mute_icon(self.musicplayer.toggle_mute())

        

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "add": self.addWidget(AddStuWidget()),
            "del":self.addWidget(DelStuWidget()),
            "mod":self.addWidget(ModStuWidget()),
            "show": self.addWidget(ShowStuWidget())
        }
        self.update_widget("add")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()

