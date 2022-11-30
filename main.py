import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from main_window import *
basedir = os.path.dirname(__file__)


if __name__ == '__main__':

    # creating the app window using main_window.py
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
