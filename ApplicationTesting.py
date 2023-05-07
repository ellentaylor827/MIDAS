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

# Test that the cursor default value in imageDisp is set to false
def testCursorDefault(mainWindow, qtbot):
    mainWindow.closeEvent = None
    assert mainWindow.imageDisp._toolbarSelection["Cursor"] == False

# Test checks that the left toolbar has a total of four actions.
def testCheckNumberOfLeftToolbarActions(mainWindow, qtbot):
    mainWindow.closeEvent = None
    assert len(mainWindow.left_toolbar.actions()) == 4, \
        f"There Should be four actions within left toolbar, hand_icon, edit_icon, comment_icon, trash_icon, their are currently {len(mainWindow.left_toolbar.actions())}"

# Check that all the actions on the left toolbar are by default set to true
def testCheckLeftToolbarActionsDefaultSetting(mainWindow, qtbot):
    mainWindow.closeEvent = None

    assert mainWindow.left_toolbar.actions()[0].isEnabled() == True, "hand_icon is set to enabled when application is first opened, Should be False"
    assert mainWindow.left_toolbar.actions()[1].isEnabled() == True, "edit_icon is set to enabled when application is first opened, Should be False"
    assert mainWindow.left_toolbar.actions()[2].isEnabled() == True, "comment_icon is set to enabled when application is first opened, should be False"



# Test that the hand button functionality works as intended when triggered
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

# Test that the edit button functionality works as intended when triggered
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

# Test that when edit icon is pressed and PanZoon is enabled, Edit is enabled and panZoom is disabled.
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

# Test that when hand icon is pressed and edit is enabled, hand icon, or panzoom is enabled and edit functionality is disabled.
def testPressHandWhileEdit(mainWindow, qtbot):
    mainWindow.closeEvent = None

    handAction = mainWindow.left_toolbar.actions()[0]
    editAction = mainWindow.left_toolbar.actions()[1]
    imageDisp = mainWindow.imageDisp

    # turn on edit functionality
    editAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "Edit Button was selected but this enabled pan/zoom aswell"
    assert imageDisp._toolbarSelection["edit"] == True, "Edit has not been enabled when selected"
    assert imageDisp._toolbarSelection["Cursor"] == False, "Edit button enabled cursor functionality"

    # turn on pan/zoom, this should disable edit.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == True, "pan/zoom functionality was not enabled when selected while edit is enabled"
    assert imageDisp._toolbarSelection["edit"] == False, "edit functionality was not disabled when selecting hand icon for pan/zoom"
    assert imageDisp._toolbarSelection["Cursor"] == False, "cursor functionality enabled when selecting hand icon while edit enabled"

    # Click hand Action again, pan/zoom should be False, edit should be False.
    handAction.trigger()
    assert imageDisp._toolbarSelection["pan/zoom"] == False, "panZoom was selected to be disabled  but it has remained enabled"
    assert imageDisp._toolbarSelection["edit"] == False, "panZoom was selected to be disabled however edit has now been enabled"
    assert imageDisp._toolbarSelection["Cursor"] == False, "panZoom was selected to be disabled however edit has been been enabled"

# Test that when a user selects a file to import, the file is stored in the right location to be opened, and imageDisplay is not set to None.
def testImageImport(mainWindow, qtbot):
    mainWindow.closeEvent = None
    mainWindow.show()


    import_action = mainWindow.file_menu.actions()[1]

    qtbot.wait(2000)
    import_action.trigger()

    ## Check that the directory is being returned to this list
    assert mainWindow.importfile_direct[0] != "", "File selected however location not stored within importfile_direct"

    assert mainWindow.imageDisp != None, "mainWindow.imageDisp not displaying image"

# Test to ensure that after a user opens the settings menu, the mainWindow.settings_window_been_open has been set to true to allow other
# functionality to work.
def testSettingsMenuRegistersOpen(mainWindow, qtbot):
    mainWindow.closeEvent = None

    settings_action = mainWindow.file_menu.actions()[2]
    settings_action.trigger()
    assert mainWindow.settings_window_been_open == True, "Settings window not set to true when it has been opened"













