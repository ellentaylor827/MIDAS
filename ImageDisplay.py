import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# ImageDisplay inherits from FigureCanvasQTAgg.
# #matplotlib FigureCanvasQTAgg allows us to have a figure to render an image to.
# The class takes a parent, a width, height and a resolution.
# After this it will set up an empty figure ready to be rendered to.


class ImageDisplay(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100,):
        # Create the Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        # connect button press event to the figure canvas
        # this button_press_event can be changed to call any self.function we want to be called
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_event)
        #self.fig.clear()

        # Create the Axes and then Hide them.
        self.axes = self.fig.add_subplot(111)
        #self.axes.clear()
        self.axes.axis('off')

        # Draw the plot.
        plt.draw()
        super(ImageDisplay, self).__init__(self.fig)



    # displayImage method takes a slice (image) and renders this to the ImageDisplay Class.
    def displayImage(self, slice):
        self.axes.clear()
        self.axes.axis('off')
        self.axes.imshow(slice)
        self.draw()

    # This function is just displaying a print statement to display the x and y being called on the button_press_event
    def mouse_event(self, event):
        print('x: {} and y: {}'.format(event.xdata, event.ydata))

    def click_event(self, e):
        print("click")
        pointCoords = e.xdata, e.ydata
        mouseClicks.append(pointCoords)  # adds points to array of all points
        if len(mouseClicks) % 2 == 0:
            # takes the last two coordinates and assigns the correct x and y values
            firstPoint = mouseClicks[-2]
            secondPoint = mouseClicks[-1]
            x = firstPoint[0], secondPoint[0]
            y = firstPoint[1], secondPoint[1]
            linePlot(x, y)

    def getGradiant(self, x, y):
        # finds the gradient on the original line
        xDifference = x[1] - x[0]
        yDifference = y[1] - y[0]
        gradient = yDifference / xDifference
        # finds perpedicular bisector gradient
        bisectorGradient = -xDifference / yDifference

    def linePlot(self, x, y):
        # plots and draws the line
        plt.plot(x, y, marker='.', color="Yellow")
        fig.canvas.draw()
        getGradiant(x, y)