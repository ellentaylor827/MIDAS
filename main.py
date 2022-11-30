import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from main_window import *
basedir = os.path.dirname(__file__)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
