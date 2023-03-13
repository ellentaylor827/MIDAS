import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import math

def linePlot(x, y, fig):
    # plots and draws the line
    plt.plot(x, y, marker='.', color="Yellow")
    fig.canvas.draw()

# used to find the gradient of the perpedicular line
def getStats(x, y):
    # finds the gradient on the original line
    print("hi")
    xDiff = x[1] - x[0]
    yDiff = y[1] - y[0]
    gradient = yDiff / xDiff
    # finds perpedicular bisector gradient
    bisectorGradient = -xDiff / yDiff
    length = math.sqrt((xDiff*xDiff) + (yDiff * yDiff))
    return (x, y, length)

# checks for mouse click
def click_event(e, fig):
    pointCoords = e.xdata, e.ydata
    mouseClicks.append(pointCoords)  # adds points to array of all points
    if len(mouseClicks) % 2 == 0:
        # takes the last two coordinates and assigns the correct x and y values
        firstPoint = mouseClicks[-2]
        secondPoint = mouseClicks[-1]
        x = firstPoint[0], secondPoint[0]
        y = firstPoint[1], secondPoint[1]
        linePlot(x, y, fig)

mouseClicks = []  # stores all line point positions
