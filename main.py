import os
import sys

import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QMenu,
    QToolBar, QStatusBar,
)

basedir = os.path.dirname(__file__)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Widgets App")
        width = 1280
        height = 720
        self.setMinimumSize(width, height)

        # Creating a slider widget, it is then set to have a range of 1 to 200. This is now set to the central widget
        # for testing but will be moved into a toolbar on the right in the future
        slider_widget = QSlider()
        slider_widget.setRange(1, 200)
        # TODO - 200 is the num of volumes we have this can be fetched as seen below:
        #  https://stackoverflow.com/questions/46712432/how-to-get-number-of-images-in-nifti-object-nibabel
        slider_widget.setSingleStep(1)
        slider_widget.valueChanged.connect(self.value_changed)
        slider_widget.sliderMoved.connect(self.slider_position)
        # This is setting the slider widget to be the central widget of the main window.
        self.setCentralWidget(slider_widget)
        # TODO - make this clickable when we have set the style and position of everything - see here:
        #  https://stackoverflow.com/questions/52689047/moving-qslider-to-mouse-click-position

        # This is creating a left toolbar that is then added to the main window. The icon size is then set to 24x24.
        # Considering increasing the icon size as it's a bit small (for macOS user's a white and black icon set might
        # be better for night mode)
        self.left_toolbar = QToolBar()
        self.left_toolbar.setIconSize(QSize(24, 24))
        print(self.left_toolbar.geometry())
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)

        # Creating 2 buttons, Hand and edit with their respective icons. We need to use filepath for any respective
        # file paths such as icons as it will not be portable when creating .exe files
        button_action2 = QAction(QIcon(os.path.join(basedir, "iconFiles", "handIcon.png")), "pan_button", self)
        button_action2.setStatusTip("Pan Button")
        button_action2.triggered.connect(self.hand_button_click)
        button_action2.setCheckable(True)
        self.left_toolbar.addAction(button_action2)
        # Creating the second button
        button_action2 = QAction(QIcon(os.path.join(basedir, "iconFiles", "editIcon.png")), "edit_button", self)
        button_action2.setStatusTip("Edit Button")
        button_action2.triggered.connect(self.edit_button_click)
        button_action2.setCheckable(True)
        self.left_toolbar.addAction(button_action2)

        # Below used to either enable or disable the status bar that we have set things such as Pan Button or Edit
        # button to

        self.setStatusBar(QStatusBar(self))

        # TODO - Make another toolbar for the right hand side and then add the slider bar to this Adding to this I
        #  need to find a way to make this code look neater and check that is in-line with the Qt formatting -
        #  Youtube might be a good aid for this.... left_toolbar.addWidget(slider_widget)

    @staticmethod
    def edit_button_click(s):
        print("The edit icon is: ", s)

    @staticmethod
    def hand_button_click(s):
        print("the hand button is: ", s)

    # Setting the right click menu items
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("undo", self))
        context.addAction(QAction("redo", self))
        context.exec(e.globalPos())

    @staticmethod
    def value_changed(i):
        print(i)

    @staticmethod
    def slider_position(p):
        print("position", p)

    @staticmethod
    def slider_pressed(self):
        print("Pressed!")

    @staticmethod
    def slider_released(self):
        print("Released")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
