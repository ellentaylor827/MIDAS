import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


# actual loading of nifty file
def loadFile(filename):
    nifty = nib.load(filename).get_fdata()
    return nifty


# placeholder function that plots and displays the file using pyplot
def showSlice(image, sliceNum):
    slice = image[:, :, sliceNum]  # selects the slice to be shown
    plt.imshow(slice, cmap=colormap)  # plots the slice onto a figure in grayscale
    plt.show()  # shows the figure
#
#
# colormap = 'gray'
# filename = "BraTS20_Training_001_t1.nii.gz"
# nifty = loadFile(filename)
# print("There are", nifty.shape[2], "slices to see.")
# sliceNum = int(input("which slice would you like to view? "))
# showSlice(nifty, sliceNum)
