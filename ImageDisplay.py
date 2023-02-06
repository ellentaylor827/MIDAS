
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

