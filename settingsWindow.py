# Creating a pyqt6 window that will hold settings for the application

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFormLayout, QVBoxLayout, QWidget, \
    QGridLayout, QComboBox, QSpinBox
from PyQt6.QtCore import (Qt, QCoreApplication, QSettings, QTranslator, QLocale, QLibraryInfo)
from PyQt6.QtGui import (QIcon, QPalette, QColor)
import sys
import os
import json

basedir = os.path.dirname(__file__)


class SettingsWindow(QWidget):

    def __init__(self):
        super().__init__()
        # set window title
        self.setWindowTitle("Settings")

        # set window size
        self.resize(300, 100)

        # Setting default values
        self.settings_file = None
        self.colourmap = None
        self.default_slice_number = None
        self.noFile = False

        # import settings from settings.json
        self.importSettings()

        # set window layout and widgets
        self.layout = QFormLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        self.combobox = QComboBox()
        # TODO - set this to the correct colourMaps - this will need to be double checked with james
        self.combobox.addItems(['gray', 'bone', 'Spectral', 'rainbow'])
        # setting the current index to the one required...
        # print("The current colourmap is: " + self.colourmap)
        if self.colourmap == "gray":
            self.combobox.setCurrentIndex(0)
        elif self.colourmap == "bone":
            self.combobox.setCurrentIndex(1)
        elif self.colourmap == "Spectral":
            self.combobox.setCurrentIndex(2)
        elif self.colourmap == "rainbow":
            self.combobox.setCurrentIndex(3)
        else:
            self.combobox.setCurrentIndex(0)

        self.combobox.currentIndexChanged.connect(self.comboboxChanged)
        label = QLabel("Colourmap:")
        # align label to the right
        self.layout.addRow(label, self.combobox)

        label_slice_number = QLabel("Default Slice:")
        self.spinner = QSpinBox()
        # this is not allowing for more than this number of slices to be displayed
        self.spinner.setRange(0, 50)
        # self.spinner.
        self.layout.addRow(label_slice_number, self.spinner)
        self.spinner.setValue(self.default_slice_number)
        self.spinner.valueChanged.connect(self.spinnerChanged)

        # save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveSettings)

        # cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        # add buttons to layout
        self.layout.addRow(self.save_button, self.cancel_button)

        # show window
        self.show()

    def spinnerChanged(self):
        self.default_slice_number = self.spinner.value()

    def comboboxChanged(self):
        self.colourmap = self.combobox.currentText()
        colourmap_outside_class = self.colourmap

    def importSettings(self):
        # import settings from settings.json
        try:
            json_file = open("settings.json", "r")
            self.settings_file = json.load(json_file)
            # loop through json file
            for key, value in self.settings_file.items():
                if key == "colourmap":
                    self.colourmap = value
                    colourmap_outside_class = self.colourmap
                elif key == "default_slice_number":
                    self.default_slice_number = value
                elif key == "setting3":
                    pass
                elif key == "setting4":
                    pass
                else:
                    self.noFile = True
                    self.showError("Error: settings file incorrect format")
            json_file.close()
            # print("colourmap: " + self.colourmap)
            # print("setting2: " + self.setting2)
        except():
            self.noFile = True
            self.showError("Error: settings file not found")

    def saveSettings(self):
        if self.noFile:
            self.showError("Error: settings file not found")
            return
        # save settings to settings.json
        self.settings_file["colourmap"] = self.colourmap
        colourmap_outside_class = self.colourmap
        self.settings_file["default_slice_number"] = self.default_slice_number
        self.settings_file["setting3"] = "test"
        self.settings_file["setting4"] = "test"
        json_file = open("settings.json", "w")
        json.dump(self.settings_file, json_file, indent=4)
        json_file.close()
        self.close()

    def showError(self, message):
        # show error message
        self.layout.addWidget(QLabel(message))
        pass

    def returnColourmap(self):
        print("return colour map function: " + self.colourmap)
        return self.colourmap

