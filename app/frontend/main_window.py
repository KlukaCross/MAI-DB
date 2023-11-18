from typing import Any, Dict

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableView, QMessageBox

from app.frontend.widgets import TablesList, EntriesTable, EntryManager
from app.backend import database


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyberpunk admin")
        self.hbox = QHBoxLayout()
        self.left_vbox = QVBoxLayout()
        self.right_vbox = QVBoxLayout()

        self.tables_list = TablesList()
        self.entries_table = EntriesTable()
        self.entry_manager: EntryManager | None = None

        update_tables_button = QPushButton("update")
        update_tables_button.clicked.connect(self.update_tables_list)

        self.create_entry_button = QPushButton("create")
        self.create_entry_button.clicked.connect(self.create_entry_manager_for_create)
        self.create_entry_button.hide()

        self.left_vbox.addWidget(update_tables_button)
        self.left_vbox.addWidget(self.tables_list)
        self.right_vbox.addWidget(self.entries_table)
        self.right_vbox.addWidget(self.create_entry_button)
        self.hbox.addLayout(self.left_vbox, 1)
        self.hbox.addLayout(self.right_vbox, 3)

        self.setLayout(self.hbox)

        self.tables_list.doubleClicked.connect(self.update_entries_table)
        self.entries_table.select_data_signal.connect(self.create_entry_manager_for_update)

        self.database = database.Database() 

    @QtCore.Slot()
    def update_tables_list(self) -> None:
        try:
            tables = self.database.get_tables()
        except ValueError as e:
            self.request_error(str(e))
            return
        self.tables_list.update_list(tables)
        self.entries_table.clear_table()
        self.create_entry_button.hide()

    @QtCore.Slot(QtCore.QModelIndex)
    def update_entries_table(self, table: QtCore.QModelIndex) -> None:
        table_name = table.data()
        self.update_entries_table_by_table_name(table_name)

    @QtCore.Slot()
    def create_entry_manager_for_create(self) -> None:
        headers = self.entries_table.headers
        self.entry_manager = EntryManager(
            fields={h: "" for h in headers},
            buttons={"create": self.create_entry}
        )
        self.entry_manager.show()

    @QtCore.Slot(object)
    def create_entry_manager_for_update(self, fields: dict[str, Any]) -> None:
        self.entry_manager = EntryManager(
            fields=fields,
            buttons={"delete": self.delete_entry, "update": self.update_entry}
        )
        self.entry_manager.show()

    @QtCore.Slot()
    def create_entry(self) -> None:
        table_name = self.tables_list.table_name
        new_fields = self.entry_manager.new_fields
        try:
            self.database.create_entry(table=table_name, values=new_fields)
        except ValueError as e:
            self.request_error(str(e))
            return
        self.update_entries_table_by_table_name(table_name)

    @QtCore.Slot()
    def update_entry(self) -> None:
        table_name = self.tables_list.table_name
        old_fields = self.entry_manager.old_fields
        new_fields = self.entry_manager.new_fields
        try:
            self.database.update_entry(table=table_name, old_values=old_fields, new_values=new_fields)
        except ValueError as e:
            self.request_error(str(e))
            return
        self.update_entries_table_by_table_name(table_name)

    @QtCore.Slot()
    def delete_entry(self) -> None:
        table_name = self.tables_list.table_name
        old_fields = self.entry_manager.old_fields
        try:
            self.database.delete_entry(table=table_name, values=old_fields)
        except ValueError as e:
            self.request_error(str(e))
            return
        self.update_entries_table_by_table_name(table_name)

    def update_entries_table_by_table_name(self, table_name: str) -> None:
        self.entry_manager = None

        try:
            headers = self.database.get_columns(table_name)
            entries = self.database.get_entries(table_name)
        except ValueError as e:
            self.request_error(str(e))
            return
        self.entries_table.update_table(table_name, headers, entries)
        self.create_entry_button.show()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.entry_manager:
            self.entry_manager.close()

    def request_error(self, error: str) -> None:
        QMessageBox.warning(self, "Request error", str(error), QMessageBox.Ok, QMessageBox.Ok)
