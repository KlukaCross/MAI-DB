from typing import Any, Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PySide6 import QtCore


class EntryManager(QWidget):
    def __init__(self, fields: dict[str, Any], buttons: dict[str, Callable]):
        super().__init__()
        self.setWindowTitle("Entry Manager")

        self._old_fields = fields

        self._vbox = QVBoxLayout()
        self._widget_fields: dict[QLabel, QLineEdit] = {}
        self._buttons: dict[QPushButton, callable] = {}

        for name, value in fields.items():
            hbox = QHBoxLayout()
            label = QLabel(name)
            line_edit = QLineEdit(value)
            self._widget_fields[label] = line_edit
            hbox.addWidget(label)
            hbox.addWidget(line_edit)
            self._vbox.addLayout(hbox)

        buttons_hbox = QHBoxLayout()
        for name, slot in buttons.items():
            button = QPushButton(name)
            buttons_hbox.addWidget(button)
            button.clicked.connect(slot)
            self._buttons[button] = slot
        self._vbox.addLayout(buttons_hbox)

        self.setLayout(self._vbox)

    @property
    def old_fields(self) -> dict[str, Any]:
        return self._old_fields

    @property
    def new_fields(self) -> dict[str, Any]:
        return {label.text(): line_edit.text() for label, line_edit in self._widget_fields.items()}
