from PySide6.QtWidgets import QListWidgetItem, QListWidget


class TablesList(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_list(self, items: list[str]) -> None:
        self.clear()
        for item in items:
            self.addItem(QListWidgetItem(item))
