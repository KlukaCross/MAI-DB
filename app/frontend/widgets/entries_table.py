from typing import Union, Any

from PySide6 import QtCore, QtWidgets, QtGui

from PySide6.QtWidgets import QTableView, QAbstractItemView, QAbstractItemDelegate, QItemDelegate
from PySide6.QtCore import QAbstractTableModel, Qt, QEvent


class EntriesTable(QTableView):
    select_data_signal = QtCore.Signal(object)

    def __init__(self):
        super().__init__()

        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        delegate = TableDelegate()
        self.setItemDelegate(delegate)
        delegate.row_select_signal.connect(self.select_row_slot)

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

    @QtCore.Slot(int)
    def select_row_slot(self, row: int):
        headers = self.model().get_headers()
        data = self.model().get_data_in_row(row)
        self.select_data_signal.emit(dict(zip(headers, data)))


class TableDelegate(QAbstractItemDelegate):
    row_select_signal = QtCore.Signal(int)

    def __init__(self):
        super().__init__()

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> None:
        QItemDelegate().paint(painter, option, index)

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: QtWidgets.QStyleOptionViewItem, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self.row_select_signal.emit(index.row())
        return False


class TableModel(QAbstractTableModel):
    def __init__(self, headers: list | None = None, data: list | None = None, *args, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)
        self._headers = headers or []
        self._data = data or []

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value)

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._headers)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._headers[section])

    def get_data_in_row(self, row: int) -> list[Any]:
        return self._data[row]

    def get_headers(self) -> list[str]:
        return self._headers
