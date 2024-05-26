from PyQt6 import QtWidgets
from WorkWidgets.MenuWidget import MenuWidget
from WorkWidgets.ShowAllWidget import ShowAllWidget
from WorkWidgets.WidgetComponents import LabelComponent, ScrollLabelComponent, LineEditComponent, ButtonComponent


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        main_layout = QtWidgets.QGridLayout()
        name_label = LabelComponent(20, content="Name", 
                                    alignment="center", bg_color=None, 
                                    font_color=None, border_color="lightgray")
        subject_label = LabelComponent(20, content="Subject", 
                                       alignment="center", bg_color=None, 
                                       font_color=None, border_color="lightgray")
        menu_label = LabelComponent(20, content="Menu", 
                                       alignment="center", bg_color=None, 
                                       font_color=None, border_color="lightgray")

        self.show_all_widget = ShowAllWidget()
        self.menu_widget = MenuWidget()

        self.menu_widget.add_student_closed.connect(self.show_all_widget.refresh_data) 
        self.menu_widget.modify_student_closed.connect(self.show_all_widget.refresh_data) 
        self.menu_widget.delete_student_closed.connect(self.show_all_widget.refresh_data)

        self.menu_widget.delete_student_closed.connect(self.refresh_main_widget)

        self.show_all_widget.selected_name_sig.connect(self.menu_widget.handle_name_clicked)

        main_layout.addWidget(name_label, 0, 0, 1, 1)
        main_layout.addWidget(subject_label, 0, 1, 1, 1)
        main_layout.addWidget(menu_label, 0, 2, 1, 1)

        main_layout.addWidget(self.show_all_widget, 1, 0, 6, 2)
        main_layout.addWidget(self.menu_widget, 4, 2, 3, 1)

        for i in range(3):
            main_layout.setColumnStretch(i, 1)
        for i in range(7):
            main_layout.setRowStretch(i, 1)

        self.setLayout(main_layout)

    def refresh_main_widget(self):
        self.menu_widget.delete_stu_button.setEnabled(False)
