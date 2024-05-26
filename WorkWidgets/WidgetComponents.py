from PyQt6 import QtWidgets, QtCore, QtGui
from functools import partial


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, alignment="left", bg_color=None, font_color=None, border_color="lightgray"):
        super().__init__()

        self.setWordWrap(True)

        if alignment == "left":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        elif alignment == "center":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        elif alignment == "right":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.setFont(QtGui.QFont("微軟正黑體", pointSize=font_size, weight=500))

        self.setText(content)
        self.setAutoFillBackground(True)
        self.setStyleSheet(f"background-color: {bg_color}; color: {font_color}; border: 1px solid {border_color};")
        

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

class ScrollLabelComponent(QtWidgets.QWidget):
    labelClicked = QtCore.pyqtSignal(str)

    def __init__(self, font_size, contents, bg_color=None, font_color=None, border_color="lightgray" ,clickable=True):
        super().__init__()

        self.font_size = font_size
        self.clickable = clickable
        self.current_label = None
        self.content = None

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(f"background-color: {bg_color}; color: {font_color}; border: 1px solid {border_color};")

        self.container = QtWidgets.QWidget()
        self.labels_layout = QtWidgets.QVBoxLayout(self.container)

        self.labels = {}
        self.add_labels(contents)

        self.scroll_area.setWidget(self.container)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
    
    def add_labels(self, contents):
        for content in contents:
            if self.clickable:
                label = ClickableLabel(content)
                label.clicked.connect(partial(self.label_clicked, content))
            else:
                label = QtWidgets.QLabel(content)
            label.setFont(QtGui.QFont("微軟正黑體", pointSize=self.font_size, weight=QtGui.QFont.Weight.Medium))
            label.setFixedHeight(30)
            label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
            label.setStyleSheet("border: 1px solid darkgray;")
            self.labels_layout.addWidget(label)
            self.labels[content] = label
        
        self.labels_layout.addStretch()

    def clear_labels(self):
        while self.labels_layout.count():
            item = self.labels_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.labels = {}
        self.current_label = None

    def label_clicked(self, content):
        if self.current_label:
            self.current_label.setStyleSheet(f"background-color: {self.current_label.default_color.name()}; border: 1px solid darkgray;")

        self.current_label = self.labels[content]
        self.current_label.setStyleSheet("background-color: darkgray; border: 1px solid darkgray;")

        self.labelClicked.emit(content)
        print(f"Label {content} clicked!")


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.text = text
        self.default_color = self.palette().color(QtGui.QPalette.ColorRole.Window)
        self.setStyleSheet(f"background-color: {self.default_color.name()}; border: 1px darkgray;")

    def mousePressEvent(self, event):
        self.clicked.emit(self.text)
        super().mousePressEvent(event)