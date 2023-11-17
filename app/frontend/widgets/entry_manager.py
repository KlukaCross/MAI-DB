from typing import Any, Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PySide6 import QtCore


class EntryManager(QWidget):
    def __init__(self, table_name: str, fields: dict[str, Any], buttons: dict[str, Callable[[str, dict[str, Any], dict[str, Any]], None]]):
        super().__init__()

        self.old_fields = fields

        self.vbox = QVBoxLayout()
        self.table_name = table_name
        self.widget_fields: dict[QLabel, QLineEdit] = {}
        self.buttons: dict[QPushButton, callable] = {}

        for name, value in fields.items():
            hbox = QHBoxLayout()
            label = QLabel(name)
            line_edit = QLineEdit(value)
            self.widget_fields[label] = line_edit
            hbox.addWidget(label)
            hbox.addWidget(line_edit)
            self.vbox.addLayout(hbox)

        buttons_hbox = QHBoxLayout()
        for name, func in buttons.items():
            button = QPushButton(name)
            buttons_hbox.addWidget(button)
            button.clicked.connect(self.activate_button_function)
            self.buttons[button] = func
        self.vbox.addLayout(buttons_hbox)

        self.setLayout(self.vbox)

    @QtCore.Slot()
    def activate_button_function(self) -> None:
        fields: dict[str, Any] = {label.text(): line_edit.text() for label, line_edit in self.widget_fields.items()}

        for button, func in self.buttons.items():
            if button.isDown():  # dont work :(
                func(self.table_name, self.old_fields, fields)
                break
