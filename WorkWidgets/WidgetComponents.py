from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, style=""):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("微軟正黑體", font_size))
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

    def disable(self):
        self.setEnabled(False)

    def enable(self):
        self.setEnabled(True)


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

    def disable(self):
        self.setEnabled(False)

    def enable(self):
        self.setEnabled(True)

class ScrollableLabelComponent(QtWidgets.QWidget):
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

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

class Mute_label(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFont(QtGui.QFont("微軟正黑體", 16))
    def set_mute_icon(self, muted):
        if muted:
            pixmap = QtGui.QPixmap("./src/mute.png")  # 加載靜音圖標
        else:
            pixmap = QtGui.QPixmap("./src/unmute.png")  # 加載取消靜音圖標
        self.setPixmap(pixmap.scaledToWidth(40))  # 設置圖標大小