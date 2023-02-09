import os
import PyQt6
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QSlider,
    QMenu,
    QToolBar, QStatusBar, QFileDialog, QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QLineEdit, QLabel
)
from niiloader import *
from ImageDisplay import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

# Setting a base directory for when generating a pyinstaller file
basedir = os.path.dirname(__file__)


# Creating a class that holds everything regarding the MainWindow and toolbars / menu items
class MainWindow(QMainWindow):
    # used later on to hold returned info from file operations
    savefile_direct = ""
    importfile_direct = ""

    # Constructor to create the MainWindow and call required items
    def __init__(self):
        # Calling the constructor of the parent class.
        super().__init__()

        # Setting buttons, icons and triggers on press for all buttons used.
        self.textbox = None
        self.imageDisp = None
        self.slider_widget = QSlider()
        self.edit_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "editIcon.png")), "Draw", self)
        self.edit_icon.triggered.connect(self.edit_button_click)
        self.edit_icon.setStatusTip("Edit Button")
        self.hand_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "handIcon.png")), "Pan", self)
        self.hand_icon.triggered.connect(self.hand_button_click)
        self.hand_icon.setStatusTip("Pan Button")
        self.undo_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "undo.png")), "Undo", self)
        self.undo_icon.triggered.connect(self.undo)
        self.redo_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "redo.png")), "Redo", self)
        self.redo_icon.triggered.connect(self.redo)
        self.save_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "save.png")), "Save", self)
        self.save_icon.triggered.connect(self.saveButtonClick)
        self.import_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "folder.png")), "Import", self)
        self.import_icon.triggered.connect(self.importButtonClick)
        self.comment_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "comment.png")), "Import", self)
        self.comment_icon.triggered.connect(self.textBoxHideButton)
        self.comment_icon.setStatusTip("Comment Button")
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
        # Call createImageDisplay to create Widget with QVboxLayout which has the navigationToolBar and
        # ImageDisplay widgets.
        self.createImageDisplay()

        self.comment_box()

    # Function - self - create a right toolbar and call the slider function to add a function to this
    def right_tool_bar(self):
        self.right_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.RightToolBarArea, self.right_toolbar)
        # add the slider to the toolbar
        self.right_toolbar.addWidget(self.slider())

    # Function - self - create the right toolbar and add pan and edit buttons
    #  These will call the edit_button_click and hand_button_click functions that can be added upon later
    def left_tool_bar(self):
        # This is creating a left toolbar that is then added to the main window. The icon size is then set to 24x24.
        # Considering increasing the icon size as it's a bit small (for macOS user's a white and black icon set might
        # be better for night mode)
        self.left_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(PyQt6.QtCore.Qt.ToolBarArea.LeftToolBarArea, self.left_toolbar)

        # Creating 2 buttons, Hand and edit with their respective icons. We need to use filepath for any respective
        # file paths such as icons as it will not be portable when creating .exe files
        self.left_toolbar.addAction(self.hand_icon)

        # Creating the second button
        self.left_toolbar.addAction(self.edit_icon)

        # Creating the comment button
        self.left_toolbar.addAction(self.comment_icon)

        # Ensuring that only 1 button (edit or pan) is selected at one time
        self.hand_icon.toggled.connect(self.edit_icon.setDisabled)
        self.edit_icon.toggled.connect(self.hand_icon.setDisabled)
        self.comment_icon.toggled.connect(self.comment_icon.setDisabled)

    def slider(self):
        # Creating a slider widget, it is then set to have a range of 1 to 200. This is now set to the central widget
        # for testing but will be moved into a toolbar on the right in the future
        self.slider_widget.setRange(1, 200)
        # TODO - set 200 to the size of the nii file after importing an image
        self.slider_widget.setSingleStep(1)
        # this thing here occurs on click and scroll - use this one for everything.
        self.slider_widget.valueChanged.connect(self.slider_value_change)

        # This thing here occurs on click - kept here if we need it in the future
        # slider_widget.sliderMoved.connect(self.slider_position)
        return self.slider_widget

    def top_main_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")
        file_menu.addAction(self.save_icon)
        file_menu.addAction(self.import_icon)
        edit_menu.addAction(self.undo_icon)
        edit_menu.addAction(self.redo_icon)
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
        # returns: ('/Users/alexanderelwell/Documents/GtiHub/MIDAS/Data File.nii',
        # 'NIFTI Images (*.nii *.nii.gz *.hdr)')
        print(savefile_direct)

    def importButtonClick(self):
        importfile_direct = self.getFileName()
        print("import button pressed!", importfile_direct)
        image_data = loadFile(importfile_direct[0])
        # Display Image
        self.imageDisp.displayImage(image_data[:, :, 45])

    # createImageDisplay method creates a QVboxlayout, Then Creates instance of ImageDisplay class.
    # Set the width height and resolution Then add the Navigationtoolbar and ImageDisplay Widgets to the layout.
    # Create a new widget and set its layout to the layout we created.
    def createImageDisplay(self):
        layout = QtWidgets.QVBoxLayout()
        self.imageDisp = ImageDisplay(self, width=20, height=20, dpi=300)
        layout.addWidget(NavigationToolbar(self.imageDisp))
        layout.addWidget(self.imageDisp)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    @staticmethod
    def color_map_setting():
        # TODO - hold all of the color map as a dropdown maybe? Or just hold the data
        end

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

        context.addAction(self.undo_icon)
        context.addAction(self.redo_icon)

        context.exec(e.globalPos())

    # this can be paired with the left click to get the location to pan the item to!
    def mouseMoveEvent(self, e):
        print("mouse moved", e.pos())

    def comment_box(self):
        # Bijoy Bakae - textbox
        layout = QVBoxLayout()
        # self.setLayout(layout)
        self.textbox = QTextEdit(self)
        self.textbox.setPlaceholderText("Enter some text")
        self.textbox.move(1050, 7)
        self.textbox.setUndoRedoEnabled(True)
        layout.addWidget(self.textbox)

    def textBoxHideButton(self):
        if self.textbox.isHidden():
            self.textbox.show()
        else:
            self.textbox.hide()

    def resizeEvent(self, event):
        self.textbox.resize(int(event.size().width() / 5), int(event.size().height() / 5))
        x = event.size().width() - self.textbox.geometry().width() - 32
        self.textbox.move(x, 65)

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

    @staticmethod
    def undo():
        print("undo")

    @staticmethod
    def redo():
        print("redo")

    def exit(self):
        self.close()
        sys.exit()

    # File handling was heavily inspired by the following source:
    # https://learndataanalysis.org/source-code-how-to-use-qfiledialog-to-select-files-in-pyqt6/ icon attribution: <a
    # href="https://www.flaticon.com/free-icons/right-arrow" title="right arrow icons">Right arrow icons created by
    # nahumam - Flaticon</a>
