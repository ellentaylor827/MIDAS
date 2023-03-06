import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

# ImageDisplay inherits from FigureCanvasQTAgg.
# #matplotlib FigureCanvasQTAgg allows us to have a figure to render an image to.
# The class takes a parent, a width, height and a resolution.
# After this it will set up an empty figure ready to be rendered to.


class ImageDisplay(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100,):

        # These are the three private member variables being created within the constructor.
        # These are all set to private as access from outside should not be required.
        self._fig = None
        self._axes = None
        self._toolbar = None
        self._toolbarSelection = {
            "pan/zoom": False,
            "edit": False
        }

        # Create the Figure
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig.clear()

        # connect button press event to the figure canvas
        # this button_press_event can be changed to call any self.function we want to be called
        self._fig.canvas.mpl_connect('button_press_event', self.mouseEvent)

        # Create the Axes and then Hide them
        self._axes = self._fig.add_subplot(111)
        #self.axes.clear()
        self._axes.axis('off')

        # Draw the plot.
        plt.draw()
        super(ImageDisplay, self).__init__(self._fig)

        # Create toolbar and attach it to the ImageDisplay and then Hide the toolbar.
        self._toolbar = NavigationToolbar(self, self)
        self._toolbar.hide()


    # displayImage method takes a slice (image) and renders this to the ImageDisplay Class.
    def displayImage(self, slice):
        self._axes.clear()
        self._axes.axis('off')
        self._axes.imshow(slice)
        self.draw()

    # This member function can be linked to a button to enable pan/zoom functionality.
    def panZoom(self):
        self._toolbar.pan()

        # If edit is set to true, call edit to set it to false.
        if self._toolbarSelection["edit"]:
            self.edit()

        # If "pan/zoom" = false, set it to true, else set it to false
        if not self._toolbarSelection["pan/zoom"]:
            self._toolbarSelection["pan/zoom"] = True
        else:
            self._toolbarSelection["pan/zoom"] = False

    def edit(self):

        # If "pan/zoom" is true, call panZoom which will call pan function and set "pan/zoom" to false.
        if self._toolbarSelection["pan/zoom"]:
            self.panZoom()

        # if "edit" = false, set it to true, else set it to false.
        if not self._toolbarSelection["edit"]:
            self._toolbarSelection["edit"] = True
        else:
            self._toolbarSelection["edit"] = False




    # This function is just displaying a print statement to display the x and y being called on the button_press_event
    def mouseEvent(self, event):
        # If edit is true, carry out the print x,y statement (or any other functionality when edit is on!)
        if self._toolbarSelection["edit"]:
            print('x: {} and y: {}'.format(event.xdata, event.ydata))



    # Code below is for reference for future line_plotting

    # def click_event(self, e):
    #     print("click")
    #     pointCoords = e.xdata, e.ydata
    #     mouseClicks.append(pointCoords)  # adds points to array of all points
    #     if len(mouseClicks) % 2 == 0:
    #         # takes the last two coordinates and assigns the correct x and y values
    #         firstPoint = mouseClicks[-2]
    #         secondPoint = mouseClicks[-1]
    #         x = firstPoint[0], secondPoint[0]
    #         y = firstPoint[1], secondPoint[1]
    #         linePlot(x, y)
    #
    # def getGradiant(self, x, y):
    #     # finds the gradient on the original line
    #     xDifference = x[1] - x[0]
    #     yDifference = y[1] - y[0]
    #     gradient = yDifference / xDifference
    #     # finds perpedicular bisector gradient
    #     bisectorGradient = -xDifference / yDifference
    #
    # def linePlot(self, x, y):
    #     # plots and draws the line
    #     plt.plot(x, y, marker='.', color="Yellow")
    #     fig.canvas.draw()
    #     getGradiant(x, y)