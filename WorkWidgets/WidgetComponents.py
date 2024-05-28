from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtWidgets import QStyle
import PyQt6.QtWidgets as QtWidgets

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("MS UI Gothic", font_size))
        self.setText(content)
        
        self.setStyleSheet( "LabelComponent { color : #333; background-color : transparent; }")

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setPlaceholderText(default_content) 
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QFont("MS UI Gothic", font_size))

        palette = QPalette(QColor("lightgray"))
        self.setPalette(palette)

        self.setStyleSheet("border: 1px solid #aaa; border-radius: 5px;")

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16, button_width=370, button_height=40):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("MS UI Gothic", font_size))

        self.setStyleSheet("""
            ButtonComponent { 
                background-color: #333; 
                color:#ddd; 
                width: 200px;
                height: 30px;
                border: none; 
                border-radius: 5px;
            }
            
            ButtonComponent:hover { 
                background-color: #666; 
            }
            """)
            
