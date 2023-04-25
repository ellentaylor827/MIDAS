import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import math

def linePlot(x, y, fig):
    # plots and draws the line
    lineTemp = plt.plot(x, y, marker='.', color="Yellow")
    #adds the drawn line to an array
    lineList.append(lineTemp)
    print(lineTemp[0].get_data())
    fig.canvas.draw()

    getStats(lineTemp[0].get_xdata(), lineTemp[0].get_ydata())

# used to find the gradient of the perpedicular line
def getStats(x, y):
    xDiff = x[1] - x[0]
    yDiff = y[1] - y[0]
    length = math.sqrt((xDiff*xDiff) + (yDiff * yDiff))
    return (x, y, length) #returns information to be displayed in window

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
    shortestDist = []
    #calculates the coordinate closest to the mouse position
    for x in range(len(mouseClicks)):
        xdist = abs(pointCoords[0] - mouseClicks[x][0])
        ydist = abs(pointCoords[1] - mouseClicks[x][1])
        hyp = math.hypot(xdist, ydist)

        if len(shortestDist) == 0:
            shortestDist.append(x)
            shortestDist.append(hyp)
        elif shortestDist[1] > hyp:
            shortestDist[0] = x
            shortestDist[1] = hyp

    closeX = mouseClicks[shortestDist[0]][0]
    closeY = mouseClicks[shortestDist[0]][1]
    for i in range(len(lineList)):
        if closeX in lineList[i][0].get_xdata() and closeY in lineList[i][0].get_ydata():
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

    getStats(currentlySelected[0].get_xdata(), currentlySelected[0].get_ydata())


# deletes a selected line
def delete_line(e):
    #removes the selected line and updates the plot
    line = lineList[0].pop(0)
    line.remove()
    plt.show()

lineList = []
mouseClicks = [] # stores all line point positions
currentlySelected = []