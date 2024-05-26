from PyQt6 import QtWidgets, QtGui
from WorkWidgets.WidgetComponents import LabelComponent
from client.ServiceCtrl import ServiceCtrl

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.service_ctrl = ServiceCtrl()
        self.service_ctrl.show_signal.connect(self.update_show)
        self.setObjectName("show_stu_widget")

        layout = QtWidgets.QVBoxLayout()
        self.setStyleSheet("background-color:transparent; border: none")
        header_label = LabelComponent(20, "Show Student") 
        layout.addWidget(header_label)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)

        self.scrollContent = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollContent.setLayout(self.scrollLayout)

        self.scrollArea.setWidget(self.scrollContent)

        self.setLayout(layout) 
    def update_show(self, data):
        print(f"Received data: {data}")
        if not data:
            return

        students = data.get('parameters', {})
        print(f"Students: {students}")

        for i in reversed(range(self.scrollLayout.count())): 
            self.scrollLayout.itemAt(i).widget().setParent(None)

        for student, details in students.items(): 
            student_details = f"\t{student}:\n"
            for score_detail in details.get('scores', []): 
                subject = score_detail.get('subject', 'Unknown')
                score = score_detail.get('score', 'Unknown')
                student_details += f"\t\t{subject}: {score}\n"

            student_label = QtWidgets.QLabel(student_details, self)
            student_label.setText(student_details)
            student_label.setFont(QtGui.QFont("Arial", 20))
            self.scrollLayout.addWidget(student_label)

    def load(self):
        data = self.service_ctrl.show()
        self.update_show(data)
        print("show widget")