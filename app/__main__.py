import sys

from PySide6 import QtWidgets

from app.frontend.main_window import MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.setMinimumSize(200, 200)
    widget.show()

    sys.exit(app.exec())
