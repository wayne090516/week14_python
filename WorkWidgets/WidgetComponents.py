from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtWidgets import QStyle
import PyQt6.QtWidgets as QtWidgets

LABEL_STYLE = """
LabelComponent {
    color : #333;
    background-color : #f2f2f2;
    font: MS UI Gothic;
}
"""
class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("MS UI Gothic", font_size))
        self.setText(content)
        
        # 修改標籤的文字顏色和背景顏色
        self.setStyleSheet( "LabelComponent { color : #333; background-color : #f2f2f2; }")

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

        # 添加一些邊框和圓角
        self.setStyleSheet("border: 1px solid #aaa; border-radius: 5px;")

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("MS UI Gothic", font_size))

        # 設置按鈕的基本樣式，然後添加一個當鼠標移上去時的動作變更樣式
        self.setStyleSheet("""
            ButtonComponent { 
                background-color: #333; 
                color:white; 
                border: none; 
                border-radius: 5px;
            }
            
            ButtonComponent:hover { 
                background-color: #666; 
            }
            """)