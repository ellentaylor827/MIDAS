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
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["pan/zoom"] == False

# Test that Edit is default False
def testEditDefault(mainWindow, qtbot):
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["edit"] == False

def testCursorDefault(mainWindow, qtbot):
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["Cursor"] == False

def testHandButton(mainWindow, qtbot):
    mainWindow.closeEvent = None

    handAction = mainWindow.left_toolbar.actions()[0]
    imageDisp = mainWindow.imageDisp

    #### Code below Simulates button press (Staying here as an example if needed).
    # qtbot.wait(2000)
    # action_rect = mainWindow.left_toolbar.actionGeometry(mainWindow.hand_icon)
    # qtbot.wait(2000)
    # qtbot.mouseMove(mainWindow.left_toolbar, action_rect.center())
    # qtbot.wait(2000)

    # Click hand Action once, pan/zoom should be True, edit should be False.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == True, "panZoom has not been enabled when selected"
    assert imageDisp._toolbarSelection["edit"] == False, "edit is enabled when panZoom has been selected"
    assert imageDisp._toolbarSelection["Cursor"] == False, "Cursor is enabled when panZoom has been selected"

    # Click hand Action again, pan/zoom should be False, edit should be False.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "panZoom was selected to be disabled  but it has remained enabled"
    assert imageDisp._toolbarSelection["edit"] == False, "panZoom was selected to be disabled however edit has now been enabled"
    assert imageDisp._toolbarSelection["Cursor"] == False, "panZoom was selected to be disabled however edit has been been enabled"

def testEditButton(mainWindow, qtbot):
    mainWindow.closeEvent = None

    editAction = mainWindow.left_toolbar.actions()[1]
    imageDisp = mainWindow.imageDisp

    # Click edit once, edit and cursor should be set to true within imageDisplay. pan/zoom should be false.
    editAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "Edit Button was selected but this enabled pan/zoom aswell"
    assert imageDisp._toolbarSelection["edit"] == True, "Edit has not been enabled when selected"
    assert imageDisp._toolbarSelection["Cursor"] == False, "Edit button enabled cursor functionality"

    # click edit once again to disable, edit and cursor should now be set false, and pan/zoom should be false.
    editAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "pan/zoom was enabled when turning off edit functionality"
    assert imageDisp._toolbarSelection["edit"] == False, "edit functionality was not disabled when selecting a second time"
    assert imageDisp._toolbarSelection["Cursor"] == False, "cursor functionality on when selecting edit to turn off"

def testPressEditWhilePanZoom(mainWindow, qtbot):
    mainWindow.closeEvent = None

    handAction = mainWindow.left_toolbar.actions()[0]
    editAction = mainWindow.left_toolbar.actions()[1]
    imageDisp = mainWindow.imageDisp

    # Turn on pan/zoom
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == True, "panZoom has not been enabled when selected"
    assert imageDisp._toolbarSelection["edit"] == False, "edit is enabled when panZoom has been selected"
    assert imageDisp._toolbarSelection["Cursor"] == False, "Cursor is enabled when panZoom has been selected"

    # Press edit button, pan/zoom should be disabled and edit functionality should be enabled.
    editAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "panZoom was not disabled when selecting edit icon"
    assert imageDisp._toolbarSelection["edit"] == True, "edit Functionality was not enabled when selected while pan/zoom is enabled"
    assert imageDisp._toolbarSelection["Cursor"] == False, "Cursor functionality turned on when selecting edit during pan/zoom"

    # click edit once again to disable, edit and cursor should now be set false, and pan/zoom should be false.
    editAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "pan/zoom was enabled when turning off edit functionality"
    assert imageDisp._toolbarSelection["edit"] == False, "edit functionality was not disabled when selecting a second time"
    assert imageDisp._toolbarSelection["Cursor"] == False, "cursor functionality on when selecting edit to turn off"














