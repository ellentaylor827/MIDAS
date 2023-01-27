import os

import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QSlider,
    QMenu,
    QToolBar, QStatusBar
)

# Setting a base directory for when generating a pyinstaller file
basedir = os.path.dirname(__file__)


# Creating a class that holds all the mainWindow data
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setting buttons / icons for the toolbar
        self.slider_widget = QSlider()
        self.edit_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "editIcon.png")), "edit_button", self)
        self.hand_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "handIcon.png")), "pan_button", self)

        # creating toolbar items
        self.left_toolbar = QToolBar()
        self.right_toolbar = QToolBar()

        # setting window title and min size (used to prevent UI being hidden from user)
        self.setWindowTitle("Widgets App")
        width = 1280
        height = 720
        self.setMinimumSize(width, height)

        # This is calling the left_tool_bar function which is then populating the left toolbar with the buttons
        self.left_tool_bar()
        self.right_tool_bar()
        self.top_main_menu()
        # Below used to either enable or disable the status bar that we have set things such as Pan Button or Edit
        # button to
        self.setStatusBar(QStatusBar(self))

    def right_tool_bar(self):
        self.right_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.RightToolBarArea, self.right_toolbar)
        # add the slider to the toolbar
        self.right_toolbar.addWidget(self.slider())

    def left_tool_bar(self):
        # This is creating a left toolbar that is then added to the main window. The icon size is then set to 24x24.
        # Considering increasing the icon size as it's a bit small (for macOS user's a white and black icon set might
        # be better for night mode)
        self.left_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)

        # Creating 2 buttons, Hand and edit with their respective icons. We need to use filepath for any respective
        # file paths such as icons as it will not be portable when creating .exe files
        self.hand_icon.setStatusTip("Pan Button")
        self.hand_icon.triggered.connect(self.hand_button_click)
        self.hand_icon.setCheckable(True)
        self.left_toolbar.addAction(self.hand_icon)

        # Creating the second button
        self.edit_icon.setStatusTip("Edit Button")
        self.edit_icon.triggered.connect(self.edit_button_click)
        self.edit_icon.setCheckable(True)
        self.left_toolbar.addAction(self.edit_icon)

        # Ensuring that only 1 button (edit or pan) is selected at one time
        self.hand_icon.toggled.connect(self.edit_icon.setDisabled)
        self.edit_icon.toggled.connect(self.hand_icon.setDisabled)

        # TODO - change so that both buttons are clickable - currently only one is then it has to be disabled to
        #  click the other

    def slider(self):
        # Creating a slider widget, it is then set to have a range of 1 to 200. This is now set to the central widget
        # for testing but will be moved into a toolbar on the right in the future
        self.slider_widget.setRange(1, 200)
        # TODO - 200 is the num of volumes we have this can be fetched as seen below:
        #  https://stackoverflow.com/questions/46712432/how-to-get-number-of-images-in-nifti-object-nibabel
        self.slider_widget.setSingleStep(1)
        # this thing here occurs on click and scroll - use this one for everything.
        self.slider_widget.valueChanged.connect(self.value_changed)

        # This thing here occurs on click - kept here if we need it in the future
        # slider_widget.sliderMoved.connect(self.slider_position)
        return self.slider_widget

    def top_main_menu(self):
        menu = self.menuBar()

        button_action = QAction("Save", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)

    def onMyToolBarButtonClick(self, s):
        print("menu is: ", s)

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
