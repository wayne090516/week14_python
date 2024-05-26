from PyQt6.QtCore import QThread, QObject, pyqtSignal

class LabelClickController(QObject):
    def __init__(self, scroll_label_component, data):
        super().__init__()
        self.data = data
        scroll_label_component.labelClicked.connect(self.handle_label_clicked)

    def handle_label_clicked(self, label_text):

        if label_text in self.data:
            print(f"Data for {label_text}: {self.data[label_text]}")
        else:
            print(f"No data found for {label_text}")

class ExecuteCommand(QThread):
    return_sig = pyqtSignal(str)

    def __init__(self, command, data):
        super().__init__()
        self.data = data
        self.command = command

    def run(self):
        result = ServiceController().command_sender(self.command, self.data)
        self.return_sig.emit(json.dumps(result))