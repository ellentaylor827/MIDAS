import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import math

def linePlot(x, y, fig):
    # plots and draws the line
    lineTemp = plt.plot(x, y, marker='.', color="Yellow")
    #adds the drawn line to an array
    lineList.append(lineTemp)
    fig.canvas.draw()

# used to find the gradient of the perpedicular line
def getStats(x, y):
    # finds the gradient on the original line
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

# calculates the closest line to the mouse position
def selectLine(e):
    pointCoords = e.xdata, e.ydata
    # calculates the closest x and y coordinate to the mouse location
    closestX = min(range(len(mouseClicks)), key=lambda x: abs(pointCoords[0] - mouseClicks[x][0]))
    closestY = min(range(len(mouseClicks)), key=lambda x: abs(pointCoords[1] - mouseClicks[x][1]))

    # calculates whether the x or y distance is closer and uses it to select the closest line
    if closestX >= closestY:
        close = mouseClicks[closestX]
        for i in range(len(lineList)):
            if close in lineList[i][0].get_xdata():
                currentlySelected.append(lineList[i][0])
                break
    else:
        close = mouseClicks[closestY]
        for i in range(len(lineList)):
            if close in lineList[i][0].get_ydata():
                currentlySelected.append(lineList[i][0])
                break

    # re-colour an already selected line and change colour of newly selected line
    if len(currentlySelected) == 0:
        pass
    elif len(currentlySelected) == 1:
        currentlySelected[0].set_color("red")
    else:
        currentlySelected[0].set_color("yellow")
        currentlySelected.pop(0)
        currentlySelected[0].set_color("red")


# deletes a selected line
def delete_line(e):
    #removes the selected line and updates the plot
    line = lineList[0].pop(0)
    line.remove()
    plt.show()

lineList = []
mouseClicks = [] # stores all line point positions
currentlySelected = []