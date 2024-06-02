from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtProperty
from PyQt6.QtGui import QFont


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, style=""):
        super().__init__()
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        
        self.setText(content)
        self.setStyleSheet(style)


class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
    
    def clear_editor_content(self, event):
        self.clear()

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

class ScrollComponent(QtWidgets.QWidget):
    def __init__(self, font_size, content, style=""):
        super().__init__()
        self.label = LabelComponent(font_size, content, style)
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def set_text(self, text):
        self.label.setText(text)

class AnimatedLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self._opacity = 1.0
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont('Arial', 24))
        
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setStyleSheet(f"color: rgba(0, 0, 0, {self._opacity});")

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("Arial", font_size))

