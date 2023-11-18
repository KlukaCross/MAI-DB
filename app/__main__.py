import sys
import os

from PySide6 import QtWidgets
from dotenv import load_dotenv


from app.frontend.main_window import MainWindow


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.setMinimumSize(200, 200)
    widget.show()

    sys.exit(app.exec())
