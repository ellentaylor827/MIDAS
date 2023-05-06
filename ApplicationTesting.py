import pytest
from PyQt5 import QtCore
import main_window
import main

@pytest.fixture
def mainWindow(qtbot):
    TestMidas = main_window.MainWindow()
    qtbot.addWidget(TestMidas)

    return TestMidas

# mainWindow.closeEvent = None is used to remove the close event for ease of testing until required.

# Test that pan/zoom are default False
def testPanZoomDefault(mainWindow, qtbot):
    mainWindow.show()
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["pan/zoom"] == False

# Test that Edit is default False
def testEditDefault(mainWindow, qtbot):
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["edit"] == False

def testHandButton(mainWindow, qtbot):
    mainWindow.closeEvent = None
    mainWindow.show()
    handAction = mainWindow.left_toolbar.actions()[0]

    imageDisp = mainWindow.imageDisp
    # qtbot.wait(2000)
    # action_rect = mainWindow.left_toolbar.actionGeometry(mainWindow.hand_icon)
    # qtbot.wait(2000)
    # qtbot.mouseMove(mainWindow.left_toolbar, action_rect.center())
    # qtbot.wait(2000)

    # Click hand Action once, pan/zoom should be True, edit should be False.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == True, "panZoom has not been enabled when selected"
    assert imageDisp._toolbarSelection["edit"] == False, "edit is enabled when panZoom has been selected"

    # Click hand Action again, pan/zoom should be False, edit should be False.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "panZoom was selected to be disabled  but it has remained enabled"
    assert imageDisp._toolbarSelection["edit"] == False, "panZoom was selected to be disabled however edit has now been enabled"