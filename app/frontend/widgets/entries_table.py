from typing import Union, Any

import PySide6

from PySide6.QtWidgets import QTableView, QAbstractItemView, QAbstractItemDelegate, QItemDelegate
from PySide6.QtCore import QAbstractTableModel, Qt, QEvent


class EntriesTable(QTableView):
    def __init__(self):
        super().__init__()

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setItemDelegate(TableDelegate())

        self.table_name = None

    def update_table(self, table_name: str, headers: list[str], data: list[list[Any]]) -> None:
        self.table_name = table_name
        model = TableModel(headers, data)
        self.setModel(model)

    def clear_table(self) -> None:
        self.setModel(TableModel())

    @property
    def headers(self) -> list[str]:
        return self.model().get_headers()


class TableDelegate(QAbstractItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionViewItem, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> None:
        QItemDelegate().paint(painter, option, index)

    def editorEvent(self, event: PySide6.QtCore.QEvent, model: PySide6.QtCore.QAbstractItemModel, option: PySide6.QtWidgets.QStyleOptionViewItem, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex]) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            print(model, option, index)
        return False


class TableModel(QAbstractTableModel):
    def __init__(self, headers: list | None = None, data: list | None = None, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)
        self._headers = headers or []
        self._data = data or []

    def data(self, index: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

    def rowCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: Union[PySide6.QtCore.QModelIndex, PySide6.QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._headers)

    def headerData(self, section: int, orientation: PySide6.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._headers[section])

    def get_headers(self) -> list[str]:
        return self._headers
