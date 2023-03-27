import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


# actual loading of nifty file
def loadFile(filename):
    nifty = nib.load(filename).get_fdata()
    # loadHeader(filename)
    return nifty


def loadFullFile(filename):
    nifty = nib.load(filename)
    print(nifty.header)
    return nifty


def loadText(filename):
    nifty = nib.load(filename)
    # stripping the formatting from the descrip field
    string_data = str(nifty.header['descrip'])
    string_data = string_data.strip("b'")
    string_data = string_data[:-1]
    return string_data


def totalAxialSlice(filename):
    nifty = nib.load(filename)
    max = nifty.header['dim'][3]
    return max


#  TODO - make this save to the nifti file and set the comment field to save to this every time it is changed - TBC -
#   set a flag to check if it has been changed - set a hard limit of 80 char to the text box
def saveText(filename, text):
    nifty = nib.load(filename)
    # max 80 char to be stored in 'descrip' field
    nifty.header['descrip'] = text
    nib.save(nifty, filename)


# TODO - delete in the future when not being used as reference to anything else

# # placeholder function that plots and displays the file using pyplot
# def showSlice(image, sliceNum, colormap):
#     slice = image[:, :, sliceNum]  # selects the slice to be shown
#     plt.imshow(slice, cmap=colormap)  # plots the slice onto a figure in grayscale
#     plt.show()  # shows the figure
#
#




# filename = "BraTS20_Training_001_t1.nii.gz"
# nifty = loadFile(filename)
# print("There are", nifty.shape[2], "slices to see.")
# sliceNum = int(input("which slice would you like to view? "))
# showSlice(nifty, sliceNum)
