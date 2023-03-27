import os
import PyQt6
import os.path
from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QAction, QIcon, QTextCursor
from PyQt6.QtWidgets import (
    QMainWindow,
    QSlider,
    QMenu,
    QToolBar, QStatusBar, QFileDialog, QWidget, QHBoxLayout, QTextEdit, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QMessageBox
)

import niiloader
from niiloader import *
from ImageDisplay import *
from settingsWindow import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2 as backendNavToolbar
import nibabel as nib
import numpy as np

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

        self.edit_menu = None
        self.file_menu = None
        self.settings_window_been_open = False
        self.settings_window = None  # No external window yet.
        # Setting buttons, icons and triggers on press for all buttons used.
        self.Panel = None
        self.text_edit = None
        self.textbox = QTextEdit()
        self.imageDisp = None
        self.Panel = QTextEdit()
        self.default_slice_number = 0
        self.toolbar = None
        self.slider_widget = QSlider()
        self.edit_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "editIcon.png")), "Draw", self)
        self.edit_icon.triggered.connect(self.edit_button_click)
        self.hand_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "handIcon.png")), "Pan", self)
        self.hand_icon.triggered.connect(self.hand_button_click)
        self.undo_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "undo.png")), "Undo", self)
        self.undo_icon.triggered.connect(self.undo)
        self.redo_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "redo.png")), "Redo", self)
        self.redo_icon.triggered.connect(self.redo)
        self.save_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "save.png")), "Save", self)
        self.save_icon.triggered.connect(self.saveButtonClick)
        self.import_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "folder.png")), "Import", self)
        self.import_icon.triggered.connect(self.importButtonClick)
        self.comment_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "content.png")), "Comment Box/Panel", self)
        self.comment_icon.triggered.connect(self.textBoxHideButton)
        self.settings_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "setting.png")), "Settings", self)
        self.settings_icon.triggered.connect(self.settingsClick)

        # TODO - assign these to the desired functions
        self.cursor_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "cursor.png")), "Cursor", self)
        self.cursor_icon.triggered.connect(self.cursorClick)
        self.trash_icon = QAction(QIcon(os.path.join(basedir, "iconFiles", "trash.png")), "Remove line", self)
        self.trash_icon.triggered.connect(self.trashClick)
        self.trash_all = QAction(QIcon(os.path.join(basedir, "iconFiles", "trash_all.png")), "Remove all lines", self)
        self.trash_all.triggered.connect(self.trashAllClick)

        # status tip
        self.status_tip()

        # creating toolbar items
        self.left_toolbar = QToolBar()
        self.right_toolbar = QToolBar()
        self.image_data = None
        # setting window title and min size (used to prevent UI being hidden from user)
        self.setWindowTitle("Widgets App")
        width = 1280
        height = 720
        self.setMinimumSize(width, height)
        self.totalAxialSlice = 0
        # This is calling the left_tool_bar function which is then populating the left toolbar with the buttons
        self.left_tool_bar()
        self.top_main_menu()

        # Below used to either enable or disable the status bar that we have set things such as Pan Button or Edit
        # button to
        self.setStatusBar(QStatusBar(self))
        # Call createImageDisplay to create Widget with QVboxLayout which has the navigationToolBar and
        # ImageDisplay widgets.
        self.createImageDisplay()

        self.initUI()

    # TODO - Temp while we assign the functions - REMOVE WHEN THE REAL FUNCTIONS HAVE BEEN ASSIGNED ABOVE
    # possible to just map the function in the below functions if multiple lines are needed to call the assigned functions :)

    def cursorClick(self):
        print("Cursor Clicked")

    def trashClick(self):
        print("Trash Clicked")

    def trashAllClick(self):
        print("Trash All Clicked")

    def initUI(self):
        # Add your widgets and layouts here

        # Connect the closeEvent signal to the closeEvent handler
        self.closeEvent = self.closeEventHandler

    def closeEventHandler(self, event):
        # Show a message box to confirm exit
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Are you sure you want to exit without saving?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        # If the user confirms exit, accept the close event and exit
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        # If the user cancels exit, ignore the close event
        else:
            self.saveButtonClick()
            event.ignore()

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

        self.left_toolbar.addAction(self.cursor_icon)
        self.left_toolbar.addAction(self.trash_icon)

        # Ensuring that only 1 button (edit or pan) is selected at one time
        self.hand_icon.toggled.connect(self.edit_icon.setDisabled)
        self.edit_icon.toggled.connect(self.hand_icon.setDisabled)
        self.comment_icon.toggled.connect(self.comment_icon.setDisabled)
        self.left_toolbar.setDisabled(True)

    def slider(self, minimum=0):
        # Creating a slider widget, it is then set to have a range of 1 to 200. This is now set to the central widget
        # for testing but will be moved into a toolbar on the right in the future
        self.slider_widget.setRange(minimum, self.totalAxialSlice - 1)
        self.slider_widget.setSingleStep(1)
        # this thing here occurs on click and scroll - use this one for everything.
        self.slider_widget.valueChanged.connect(self.slider_value_change)
        # This thing here occurs on click - kept here if we need it in the future
        # slider_widget.sliderMoved.connect(self.slider_position)
        return self.slider_widget

    def top_main_menu(self):
        menu = self.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.edit_menu = menu.addMenu("&Edit")
        self.file_menu.addAction(self.save_icon)
        self.file_menu.addAction(self.import_icon)
        self.file_menu.addAction(self.settings_icon)
        self.edit_menu.addAction(self.undo_icon)
        self.edit_menu.addAction(self.redo_icon)
        self.edit_menu.addAction(self.edit_icon)
        self.edit_menu.addAction(self.hand_icon)
        self.edit_menu.addAction(self.cursor_icon)
        self.edit_menu.addAction(self.trash_icon)
        self.edit_menu.addAction(self.trash_all)
        self.edit_menu.addAction(self.comment_icon)
        self.edit_menu.setDisabled(True)
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
        # Check that a file has been selected and stored in tuple index 0
        # if it is empty, cancel or nothing has been selected, pass to avoid crash
        if savefile_direct[0] == "":
            pass
        else:
            print(self.image_data)
            self.saveFile(savefile_direct[0], self.image_data)

    # Save the file to the specified location
    def saveFile(self, filename, data):
        # add a check to see if the file already exists and if it does, ask the user if they want to overwrite it
        if (os.path.exists(filename)):
            print("File already exists")
        else:
            print("File does not exist")

        # add a check to see if the file is a nifti file and if it is not, add the appropriate extension
        if(filename.endswith('.nii') or filename.endswith('.nii.gz') or filename.endswith('.hdr')):
            print("File is a nifti file")
        else:
            filename.join('.nii')
            print("File is not a nifti file")
        original = niiloader.loadFullFile(self.importfile_direct[0])
        # Create a new .nii file with the modified data
        data[0,0,0] = float(360.0)
        print("This is the thing ehre")
        print(line_plot.lineList)
        for i in range(len(line_plot.lineList)):
            print(line_plot.lineList[i])
        #     TODO - add the line data to the data variable 

        new_img = nib.Nifti1Image(data, original.affine, original.header)
        nib.save(new_img, filename)

    def importButtonClick(self):
        settings = SettingsWindow()
        default_slice = settings.default_slice_number
        self.importfile_direct = self.getFileName()
        print("import button pressed!", self.importfile_direct)

        # Check that a file has been selected and stored in tuple index 0
        # if it is empty, cancel or nothing has been selected, pass to avoid crash
        if self.importfile_direct[0] == "":
            pass
        else:
            self.image_data = loadFile(self.importfile_direct[0])
            # Display Image
            self.DisplayImageSlice(default_slice)
            self.totalAxialSlice = niiloader.totalAxialSlice(self.importfile_direct[0])
            self.right_tool_bar()
            self.left_toolbar.setEnabled(True)
            self.edit_menu.setEnabled(True)
            self.comment_box()
            self.Stat_Panel()
            # hack - this is a hack to get the comment and stat panel to show up correctly
            self.resize(1285, 725)
            self.slider_widget.setValue(default_slice)

    def DisplayImageSlice(self, i):
        self.imageDisp.displayImage(self.image_data[:, :, i])

    # createImageDisplay method creates a QVboxlayout, Then Creates instance of ImageDisplay class.
    # Set the width height and resolution Then add the Navigationtoolbar and ImageDisplay Widgets to the layout.
    # Create a new widget and set its layout to the layout we created.
    def createImageDisplay(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.imageDisp = ImageDisplay(self, width=20, height=20, dpi=300)
        # layout.addWidget(NavigationToolbar(self.imageDisp))
        self.layout.addWidget(self.imageDisp)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    @staticmethod
    def color_map_setting():
        # TODO - hold all of the color map as a dropdown maybe? Or just hold the data
        pass

    def edit_button_click(self):
        # make sure that this will first disable the pan/hand button
        print("Edit button pressed!")
        self.imageDisp.edit()

    def hand_button_click(self):
        # make sure that this will first disable the edit button
        print("hand button clicked!")
        # TODO - make sure that this will first disable the drawing button
        self.imageDisp.panZoom()

    # this can be paired with the left click to get the location to pan the item to!
    def mouseMoveEvent(self, e):
        print("mouse moved", e.pos())

    def comment_box(self):
        # Bijoy Bakar - textbox
        layout = QVBoxLayout()
        # self.setLayout(layout)
        self.textbox = QTextEdit(self)
        if not self.importfile_direct:
            self.textbox.setPlaceholderText("Enter text here")
        else:
            self.textbox.setText(loadText(self.importfile_direct[0]))
        # print textbox data
        self.textbox.textChanged.connect(self.on_text_box_change)
        self.textbox.move(1050, 7)
        self.textbox.setUndoRedoEnabled(True)
        self.textbox.textChanged.connect(self.limit_text)
        layout.addWidget(self.textbox)

    def limit_text(self):
        text = self.textbox.toPlainText()
        words = text.split()
        if len(words) > 80:
            self.textbox.setPlainText(" ".join(words[:80]))
            self.textbox.setReadOnly(True)
        else:
            self.textbox.setReadOnly(False)

    def on_text_box_change(self):
        niiloader.saveText(self.importfile_direct[0], self.textbox.toPlainText())
        print(self.textbox.toPlainText())

    def textBoxHideButton(self):
        if self.textbox.isHidden():
            self.textbox.show()
            self.Panel.show()
        else:
            self.textbox.hide()
            self.Panel.hide()

    def resizeEvent(self, event):
        # Comment Box
        self.textbox.resize(int(event.size().width() / 5), int(event.size().height() / 5))
        x = event.size().width() - self.textbox.geometry().width() - 13
        self.textbox.move(x, 11)

        # Stat Panel
        self.Panel.resize(int(event.size().width() / 5), int(event.size().height() / 6.5))
        x = event.size().width() - self.Panel.geometry().width() - 13
        y = self.textbox.geometry().y() + self.textbox.geometry().height()
        self.Panel.move(x, y)

    def mousePressEvent(self, e):
        print("mouse pressed")

    # will be used to free the mouse from the pan or select tools
    def mouseReleaseEvent(self, e):
        print("Mose released")

    def mouseDoubleClickEvent(self, e):
        print("mouse double clicked")

    def slider_value_change(self, i):
        print("slider value changed" + str(self.settings_window_been_open))
        if self.settings_window_been_open:
            self.settings_window_closed()
            self.settings_window_been_open = False
        self.DisplayImageSlice(i)

    @staticmethod
    def undo():
        print("undo")

    @staticmethod
    def redo():
        print("redo")

    def exit(self):
        self.close()
        sys.exit()

    # bijoy
    def status_tip(self):
        self.hand_icon.setStatusTip("Pan Button")
        self.edit_icon.setStatusTip("Edit Button")
        self.slider_widget.setStatusTip("Slider")
        self.comment_icon.setStatusTip("Comment Box/Panel")
        self.save_icon.setStatusTip("Save")
        self.import_icon.setStatusTip("Import")
        self.redo_icon.setStatusTip("Redo")
        self.undo_icon.setStatusTip("Undo")

    def Stat_Panel(self):
        # Bijoy Bakar - `Stat Panel
        layout = QVBoxLayout()
        self.Panel = QTextEdit(self)
        # this is how you would add the values text_box.setText(f"The value is {value}")
        self.Panel.setText("Diameter: \n\nX-Coordinates:  \n\nY-Coordinates: ")
        self.Panel.setReadOnly(True)
        layout.addWidget(self.Panel)

    # settings window
    # Setting to None to prevent more than one settings window from opening at a time - prevents settings JSON being
    # written to multiple times
    def settingsClick(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        #         on window close run a function...
        self.settings_window_been_open = True

    def settings_window_closed(self):
        # reload the image to apply the settings
        if self.totalAxialSlice == 0:
            print("no image open")
            pass
        else:
            print("image open")
            self.layout.removeWidget(self.imageDisp)
            self.imageDisp = ImageDisplay(self, width=20, height=20, dpi=300)
            self.layout.addWidget(self.imageDisp)

# File handling was heavily inspired by the following source:
# https://learndataanalysis.org/source-code-how-to-use-qfiledialog-to-select-files-in-pyqt6/ icon attribution: <a
# href="https://www.flaticon.com/free-icons/right-arrow" title="right arrow icons">Right arrow icons created by
# nahumam - Flaticon</a>
