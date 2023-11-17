from typing import Any

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableView

from app.frontend.widgets import TablesList, EntriesTable, EntryManager
from app.backend import handlers


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Cyberpunk admin")
        self.hbox = QHBoxLayout()
        self.left_vbox = QVBoxLayout()
        self.right_vbox = QVBoxLayout()

        self.tables_list = TablesList()
        self.entries_table = EntriesTable()
        self.entry_manager = None

        update_tables_button = QPushButton("update")
        update_tables_button.clicked.connect(self.update_tables_list)

        self.create_entry_button = None

        self.left_vbox.addWidget(update_tables_button)
        self.left_vbox.addWidget(self.tables_list)
        self.right_vbox.addWidget(self.entries_table)
        self.hbox.addLayout(self.left_vbox)
        self.hbox.addLayout(self.right_vbox)

        self.setLayout(self.hbox)

        self.tables_list.doubleClicked.connect(self.update_entries_table)

    @QtCore.Slot()
    def update_tables_list(self) -> None:
        tables = handlers.get_tables()
        self.tables_list.update_list(tables)

    @QtCore.Slot(QtCore.QModelIndex)
    def update_entries_table(self, table: QtCore.QModelIndex) -> None:
        table_name = table.data()
        headers = handlers.get_columns(table_name)
        entries = handlers.get_entries(table_name)
        self.entries_table.update_table(table_name, headers, entries)
        if not self.create_entry_button:
            self.create_entry_button = QPushButton("create")
            self.create_entry_button.clicked.connect(self.create_entry_manager_for_create)
        self.right_vbox.addWidget(self.create_entry_button)

    @QtCore.Slot()
    def create_entry_manager_for_create(self) -> None:
        table_name = self.tables_list.selectedItems()[0].text()
        headers = self.entries_table.model().get_headers()
        self.entry_manager = EntryManager(
            table_name=table_name,
            fields={h: "" for h in headers},
            buttons={"create": self.create_entry}
        )
        self.entry_manager.show()

    @QtCore.Slot()
    def create_entry_manager_for_update(self) -> None:
        table_name = self.tables_list.selectedItems()[0].text()
        headers = self.entries_table.model().get_headers()
        self.entry_manager = EntryManager(
            table_name=table_name,
            fields={h: "" for h in headers},
            buttons={"delete": self.delete_entry, "update": self.update_entry}
        )
        self.entry_manager.show()

    def create_entry(self, table_name: str, old_fields: dict[str, Any], new_fields: dict[str, Any]) -> None:
        print("create entry!")

    def update_entry(self, table_name: str, old_fields: dict[str, Any], new_fields: dict[str, Any]) -> None:
        print("update entry!")

    def delete_entry(self, table_name: str, old_fields: dict[str, Any], new_fields: dict[str, Any]) -> None:
        print("delete entry!")
