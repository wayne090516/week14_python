from WorkWidgets.MainWidget import MainWidget
from PyQt6.QtWidgets import QApplication
from PyQt6 import sip
import sys

app = QApplication([])
main_window = MainWidget()

main_window.setFixedSize(730, 350)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec())
