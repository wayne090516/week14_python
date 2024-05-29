from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize
from functools import partial

class BackgroundImageSetter:
    def __init__(self, widget, image_path):
        self.widget = widget
        self.image_path = image_path

    def paint_background(self, painter):
        oImage = QtGui.QPixmap(self.image_path)
        sImage = oImage.scaled(self.widget.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding, QtCore.Qt.TransformationMode.SmoothTransformation)
        # Calculate the center crop area
        x = max(0, (sImage.width() - self.widget.width()) // 2)
        y = max(0, (sImage.height() - self.widget.height()) // 2)
        painter.drawPixmap(0, 0, sImage.copy(x, y, self.widget.width(), self.widget.height()))

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content, alignment="left", style=None, image_path=None):
        super().__init__()

        self.setWordWrap(True)

        if alignment == "left":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        elif alignment == "center":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        elif alignment == "right":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.setFont(QtGui.QFont("微軟正黑體", pointSize=font_size, weight=1000))

        self.setText(content)
        self.setAutoFillBackground(False)
        
        if style:
            self.setStyleSheet(style)
        
        self.bg_setter = None
        if image_path:
            self.bg_setter = BackgroundImageSetter(self, image_path)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        radius = 10
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        if self.bg_setter:
            self.bg_setter.paint_background(painter)
        
        painter.setClipping(False)
        super().paintEvent(event)

    def resizeEvent(self, event):
        self.update()
        super().resizeEvent(event)
        
class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, font_size=16, default_content="", alignment="left", style=None):
        super().__init__()

        if alignment == "left":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        elif alignment == "center":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        elif alignment == "right":
            self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        # self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        # self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

        if style:
            self.setStyleSheet(style)

    def clear_editor_content(self, event):
        self.clear()

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, font_size=16, content="",style=None):
        super().__init__()
        self.setText(content)
        self.setFont(QtGui.QFont("微軟正黑體", font_size, weight=1000))

        self.default_style = style
        
        self.disabled_style = """
            QPushButton:disabled {
                color: red;
            }
        """

        self.setStyleSheet(self.default_style + self.disabled_style)

    def resizeEvent(self, event):
        self.update()
        super().resizeEvent(event)

class ScrollLabelComponent(QtWidgets.QWidget):
    labelClicked = QtCore.pyqtSignal(str)

    def __init__(self, font_size, contents, clickable=True, style=None):
        super().__init__()

        self.font_size = font_size
        self.clickable = clickable
        self.current_label = None
        self.content = None

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(style)

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
            label.setStyleSheet("background: #c0c0c0; color: #404040; border-radius: 5px;")
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
            self.current_label.setStyleSheet("background: #c0c0c0; color: #404040; border-radius: 5px;")

        self.current_label = self.labels[content]
        self.current_label.setStyleSheet("background: #a0a0a0; color: #404040; border-radius: 5px;")

        self.labelClicked.emit(content)
        # print(f"Label {content} clicked!")

    def resizeEvent(self, event):
        self.update()
        super().resizeEvent(event)

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.text = text
        self.default_color = self.palette().color(QtGui.QPalette.ColorRole.Window)
        self.setStyleSheet(f"background-color: {self.default_color.name()}; border-radius: 5px;")
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        self.clicked.emit(self.text)
        super().mousePressEvent(event)

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, font_size=16, style=None):
        super().__init__()
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setMinimumSize(150, 30)
        if style:
            self.setStyleSheet(style)
