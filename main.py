# import needed files
import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from main_window import *
# setting base directory for os
basedir = os.path.dirname(__file__)


if __name__ == '__main__':
    # creating the app window using main_window.py
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    