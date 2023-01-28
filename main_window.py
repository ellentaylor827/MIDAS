import os

import PyQt6
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QSlider,
    QMenu,
    QToolBar, QStatusBar, QFileDialog
)

# Setting a base directory for when generating a pyinstaller file
basedir = os.path.dirname(__file__)


# Creating a class that holds everything regarding the mainwindow and tool bars / menu items
class MainWindow(QMainWindow):
    # used later on to hold returned info from file operations
    savefile_direct = ""
    importfile_direct = ""

    # Constructor to create the mainwindow and call required items
    def __init__(self):
        # Calling the constructor of the parent class.
        super().__init__()

        # self.setMouseTracking(True)

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

    # Function - self - create a right tool bar and call the slider function to add a function to this
    def right_tool_bar(self):
        self.right_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.RightToolBarArea, self.right_toolbar)
        # add the slider to the toolbar
        self.right_toolbar.addWidget(self.slider())

    # Function - self - create the right tool bar and add pan and edit buttons
    #  These will call the edit_button_click and hand_button_click functions that can be added upon later
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
        self.left_toolbar.addAction(self.hand_icon)

        # Creating the second button
        self.edit_icon.setStatusTip("Edit Button")
        self.edit_icon.triggered.connect(self.edit_button_click)
        self.left_toolbar.addAction(self.edit_icon)

        # Ensuring that only 1 button (edit or pan) is selected at one time
        self.hand_icon.toggled.connect(self.edit_icon.setDisabled)
        self.edit_icon.toggled.connect(self.hand_icon.setDisabled)

    def slider(self):
        # Creating a slider widget, it is then set to have a range of 1 to 200. This is now set to the central widget
        # for testing but will be moved into a toolbar on the right in the future
        self.slider_widget.setRange(1, 200)
        # TODO - 200 is the num of volumes we have this can be fetched as seen below:
        #  https://stackoverflow.com/questions/46712432/how-to-get-number-of-images-in-nifti-object-nibabel
        self.slider_widget.setSingleStep(1)
        # this thing here occurs on click and scroll - use this one for everything.
        self.slider_widget.valueChanged.connect(self.slider_value_change)

        # This thing here occurs on click - kept here if we need it in the future
        # slider_widget.sliderMoved.connect(self.slider_position)
        return self.slider_widget

    def top_main_menu(self):
        menu = self.menuBar()

        # Save button
        button_action = QAction("Save", self)
        button_action.setStatusTip("This is to save the file")
        button_action.triggered.connect(self.saveButtonClick)

        # import button
        import_action = QAction("Import", self)
        import_action.setStatusTip("This is to import a file")
        import_action.triggered.connect(self.importButtonClick)

        # File menu
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")
        file_menu.addAction(button_action)
        file_menu.addAction(import_action)
        edit_menu.addAction(self.edit_icon)
        edit_menu.addAction(self.hand_icon)

    # Function - self - to get a file name
    def getFileName(self):
        file_filter = 'NIFTI Images (*.nii *.nii.gz *.hdr)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='NIFTI Images (*.nii *.nii.gz *.hdr)'
        )
        return response

    # Function - self - to get multiple file names
    def getFileNames(self):
        file_filter = 'NIFTI Images (*.nii *.nii.gz *.hdr)'
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select file(s)',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='NIFTI Images (*.nii *.nii.gz *.hdr)'
        )
        return response

    # Function - self - to get a name and place to save a file
    def getSaveFileName(self):
        file_filter = 'NIFTI Images (*.nii *.nii.gz *.hdr) ;; All Files (*)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            # TODO - make sure that this is the data type that we want to return (nii, nii.gz or what?)
            directory='Data File.nii',
            filter=file_filter,
            initialFilter='NIFTI Images (*.nii *.nii.gz *.hdr)'
        )
        return response

    def saveButtonClick(self):
        savefile_direct = self.getSaveFileName()
        print("save button pressed!")

    def importButtonClick(self):
        importfile_direct = self.getFileName()
        print("import button pressed!")

    @staticmethod
    def edit_button_click():
        # make sure that this will first disable the pan/hand button
        print("Edit button pressed!")

    @staticmethod
    def hand_button_click():
        # make sure that this will first disable the edit button
        print("hand button clicked!")

    # Setting the right click menu items
    def contextMenuEvent(self, e):
        context = QMenu(self)
        undo_action = QAction("undo", self)
        undo_action.triggered.connect(self.undo)
        context.addAction(undo_action)
        redo_action = QAction("redo", self)
        redo_action.triggered.connect(self.redo)
        context.addAction(redo_action)
        context.exec(e.globalPos())

    # TODO - these are the functions that we need to implement for the mouse events such as
    #  double click to add a point for the line
    #  left mouse and move to pan

    # this can be paired with the left click to get the location to pan the item to!
    def mouseMoveEvent(self, e):
        print("mouse moved", e.pos())

    def mousePressEvent(self, e):
        print("mouse pressed")

    # will be used to free the mouse from the pan or select tools
    def mouseReleaseEvent(self, e):
        print("Mose released")

    def mouseDoubleClickEvent(self, e):
        print("mouse double clicked")

    @staticmethod
    def slider_value_change(i):
        print(i)

    def undo(self):
        print("undo")

    def redo(self):
        print("redo")

    # KEEP THIS HERE COS IDK IF WE NEED IT
    # @staticmethod
    # def slider_position(p):
    #     print("position", p)

    # File handling was heavily inspired by the following source:
    # https://learndataanalysis.org/source-code-how-to-use-qfiledialog-to-select-files-in-pyqt6/
