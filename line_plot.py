import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def linePlot(x, y):
    #plots and draws the line
    plt.plot(x, y, marker='.', color="Yellow")
    fig.canvas.draw()

#checks for mouse click
def click_event(e):
    pointCoords = e.xdata, e.ydata
    mouseClicks.append(pointCoords) #adds points to array of all points
    if len(mouseClicks) % 2 == 0:
        #takes the last two coordinates and assigns the correct x and y values
        firstPoint = mouseClicks[-2]
        secondPoint = mouseClicks[-1]
        x = firstPoint[0], secondPoint[0]
        y = firstPoint[1], secondPoint[1]
        linePlot(x, y)

#create a mouse click event
fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', click_event) #creates the click event
mouseClicks = [] #stores all line point positions



