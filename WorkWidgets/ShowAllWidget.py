from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QEventLoop
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ScrollLabelComponent
from client.ServiceController import ExecuteCommand
import json

class ShowAllWidget(QtWidgets.QWidget):
    selected_name_sig = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("show_all_widget")

        self.names = []
        self.result = {}
        self.subjects_dict = {}

        self.show_all_layout = QtWidgets.QGridLayout()
        self.names, self.subjects_dict = self.get_refreshed_data()
        self.name_scroll_label = ScrollLabelComponent(14, self.names, 
                                                        bg_color=None, font_color=None, 
                                                        border_color="lightgray", clickable=True)
        self.name_scroll_label.labelClicked.connect(self.handle_name_clicked)

        self.subject_scroll_label = ScrollLabelComponent(14, [], 
                                                         bg_color=None, font_color=None, 
                                                         border_color="lightgray", clickable=True)

        self.show_all_layout.addWidget(self.name_scroll_label, 0, 0)
        self.show_all_layout.addWidget(self.subject_scroll_label, 0, 1)

        for i in range(2):
            self.show_all_layout.setColumnStretch(i, 1)

        self.setLayout(self.show_all_layout)
        self.selected_name = None

    def refresh_data(self):
        self.names, self.subjects_dict = self.get_refreshed_data()
        self.name_scroll_label.clear_labels()
        self.name_scroll_label.add_labels(self.names)
        self.subject_scroll_label.clear_labels()

    def get_refreshed_data(self):
        self.execute_show = ExecuteCommand(command="show", data={})
        self.execute_show.return_sig.connect(self.show_action_result)
        
        self.loop = QEventLoop()
        self.execute_show.return_sig.connect(self.loop.quit)
        
        self.execute_show.start()
        self.loop.exec() 
        
        return self.names, self.subjects_dict

    def show_action_result(self, result):
        self.result = eval(json.loads(result))
        student_dict = self.result["parameters"]

        self.names = []
        self.subjects_dict = {}
        subject_cluster = []

        for key, value in student_dict.items():
            self.names.append(key)
            subject_cluster = []
            for subject, score in value["scores"].items():
                subject_cluster.append(f"{subject}:{score}")
            self.subjects_dict[key] = subject_cluster

    def handle_name_clicked(self, label_content):
        self.selected_name_sig.emit(label_content)
        self.selected_name = label_content
        self.clicked_show_subject(label_content)

    def clicked_show_subject(self, label_content):
        subjects = self.subjects_dict.get(label_content, [])
        self.subject_scroll_label.clear_labels()
        self.subject_scroll_label.add_labels(subjects)

    # def get_selected_subject(self):
    #     return self.subject_scroll_label.current_label.text() if self.subject_scroll_label.current_label else None