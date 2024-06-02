from WorkWidgets.MainWidget import MainWidget
from PyQt6.QtWidgets import QApplication
from client.ServiceControl import ServiceControl
import sys

app = QApplication([])
socket_client = ServiceControl()
main_window = MainWidget(socket_client)
main_window.setFixedSize(700, 350)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec())
