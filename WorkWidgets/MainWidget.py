from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSlider, QMainWindow
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QMovie
from PyQt6.QtCore import Qt, QSize
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.Music import Music
from WorkWidgets.WidgetComponents import *
from client.ServiceCtrl import ServiceCtrl
import threading
import sys
import os

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("main_widget")

        layout = QtWidgets.QGridLayout()
        function_widget = FunctionWidget()
        menu_widget = MenuWidget(function_widget.update_widget)
        
        self.setWindowTitle('Student Management System')
        layout.addWidget(menu_widget, 0, 0, 8, 8)
        layout.addWidget(function_widget, 1, 1, 1, 2)

        self.movie = QMovie("WorkWidgets/source/pic01.gif")
        label = QLabel(self)
        label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(label, 1, 3, 1, 1)

        oImage = QPixmap("WorkWidgets/source/pic02.jpg")
        sImage = oImage.scaled(QSize(1200,600))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.setColumnStretch(3, 4)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 6)
        layout.setRowStretch(2, 1)

        self.setLayout(layout)
        self.menu_widget = menu_widget

    def closeEvent(self, event):
        self.menu_widget.stop_music()
        event.accept()

class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QGridLayout()
        add_button = ButtonComponent("Add student")
        show_button = ButtonComponent("Home")
        del_button = ButtonComponent("Delete student")
        modify_button = ButtonComponent("Modify student")
        # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))

        self.music = Music(os.path.join(os.getcwd(), "WorkWidgets/source/music.mp3")) 
        
        self.volume_slider = QSlider(Qt.Orientation.Vertical)  
        self.volume_slider.setValue(100)
        self.volume_slider.setMinimum(0) 
        self.volume_slider.setMaximum(100) 
        self.volume_slider.valueChanged.connect(self.music.set_volume) 
        self.volume_slider.setFixedWidth(20)
        set_volume = LabelComponent(14, "volume")

        self.music_thread = threading.Thread(target=self.start_music)
        self.music_thread.start()

        layout.addWidget(show_button, 0,0,1,1)
        layout.addWidget(self.volume_slider,1,0,1,1)
        layout.addWidget(set_volume, 2,0,1,1)
        layout.addWidget(add_button, 2,1,1,1)
        layout.addWidget(del_button, 2,2,1,1)
        layout.addWidget(modify_button, 2,3,1,1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 2)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 6)
        layout.setRowStretch(2, 1)

        self.setLayout(layout)

    def start_music(self):
        self.music.play()
        self.music_playing = True

    def stop_music(self):
        self.music.stop()  
        self.music_playing = False


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.widget_dict = {
            "add": self.addWidget(AddStuWidget()),
            "show": self.addWidget(ShowStuWidget()),
            "del": self.addWidget(DelStuWidget()),
            "modify": self.addWidget(ModifyStuWidget())
        }
        self.update_widget("show")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
