
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# Edit SeamCarving.ipynb instead.
from hashlib import new
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, signal
from imageio import imread, imsave

def  rgb2gray(img):
    """
    Converts an RGB image into a greyscale image

    Input: ndarray of an RGB image of shape (H x W x 3)
    Output: ndarray of the corresponding grayscale image of shape (H x W)

    """

    if(img.ndim != 3 or img.shape[-1] != 3):
        print("Invalid image! Please provide an RGB image of the shape (H x W x 3) instead.".format(img.ndim))
        return None

    return np.dot(img[...,:3], [0.2989, 0.5870, 0.1140])

def compute_gradients(img):
    """
    Computes the gradients of the input image in the x and y direction using a
    differentiation filter.

    ##########################################################################
    # TODO: Design a differentiation filter and update the docstring. Stick  #
    # to a pure differentiation filter for this assignment.                  #
    # Hint: Look at Slide 14 from Lecture 3: Gradients.                      #
    ##########################################################################

    Input: Grayscale image of shape (H x W)
    Outputs: gx, gy gradients in x and y directions respectively

    """
    xfilter = [[1,0,-1],
               [1,0,-1],
               [1,0,-1]]

    yfilter = [[1,1,1],
               [0,0,0],
               [-1,-1,-1]]


    gx = gy = np.zeros_like(img)

    ##########################################################################
    # TODO: Design a pure differentiation filter and use correlation to      #
    # compute the gradients gx and gy. You might have to try multiple        #
    # filters till the test below passes. All the tests after will fail if   #
    # this one does not pass.                                                #
    ##########################################################################
    #gradient = np.gradient(img)
    gx = ndimage.correlate(img, xfilter, mode = 'constant', cval = 0.0)
    gy = ndimage.correlate(img, yfilter, mode = 'constant', cval = 0.0)
    return gx, gy

def energy_image(img):
    """
    Computes the energy of the input image according to the energy function:

        e(I) = abs(dI/dx) + abs(dI/dy)

    Use compute_gradients() to help you calculate the energy image. Remember to normalize
    energyImage by dividing it by max(energyImage).

    Input: image of the form (H x W) or (H x w x 3)
    Output: array of energy values of the image computed according to the energy function.

    """
    energyImage = np.zeros_like(img)

    ##########################################################################
    # TODO: Compute the energy of input using the defined energy function.   #                                             #
    ##########################################################################
    if len(img.shape) == 2:
        gx, gy = compute_gradients(img)
        energyImage = abs(gx) + abs(gy)
        energyImage = energyImage / np.amax(energyImage)
        return energyImage
    else:
        grayImg = rgb2gray(img)
        gx, gy = compute_gradients(grayImg)
        energyImage = abs(gx) + abs(gy)
        energyImage = energyImage / np.amax(energyImage)
        return energyImage

def cumulative_minimum_energy_map(energyImage, seamDirection):
    """
    Calculates the cumulative minim energy map according to the function:

        M(i, j) = e(i, j) + min(M(i-1, j-1), M(i-1, j), M(i-1, j+1))

    Inputs:
        energyImage: Results of passign the input image to energy_image()
        seamDirection: 'HORIZONTAL' or 'VERTICAL'

    Output: cumulativeEnergyMap

    """

    cumulativeEnergyMap = np.zeros_like(energyImage)

    ##########################################################################
    # TODO: Compute the cumulative minimum energy map in the input           #
    # seamDirection for the input energyImage. It is fine it is not fully    #
    # vectorized.                                                            #
    ##########################################################################
    if (seamDirection == "VERTICAL"):
        rowLength = len(cumulativeEnergyMap[0])
        cumulativeEnergyMap[0] = energyImage[0]
        for i in range(1,len(cumulativeEnergyMap)):
            for j in range(rowLength):
                if j == 0:
                    cumulativeEnergyMap[i][j] = energyImage[i][j] + min(cumulativeEnergyMap[i-1,j], cumulativeEnergyMap[i-1,j+1])
                elif j == rowLength - 1:
                    cumulativeEnergyMap[i][j] = energyImage[i][j] + min(cumulativeEnergyMap[i-1,j-1], cumulativeEnergyMap[i-1,j])
                else:
                    cumulativeEnergyMap[i][j] = energyImage[i][j] + min(cumulativeEnergyMap[i-1,j-1], cumulativeEnergyMap[i-1,j], cumulativeEnergyMap[i-1,j+1])

    elif (seamDirection == "HORIZONTAL"):
        cumulativeEnergyMap = cumulativeEnergyMap.transpose()
        mapTranspose = energyImage.transpose()
        rowLength = len(cumulativeEnergyMap[0])
        cumulativeEnergyMap[0] = mapTranspose[0]
        for i in range(1,len(cumulativeEnergyMap)):
            for j in range(rowLength):
                if j == 0:
                    cumulativeEnergyMap[i][j] = mapTranspose[i][j] + min(cumulativeEnergyMap[i-1,j], cumulativeEnergyMap[i-1,j+1])
                elif j == rowLength - 1:
                    cumulativeEnergyMap[i][j] = mapTranspose[i][j] + min(cumulativeEnergyMap[i-1,j-1], cumulativeEnergyMap[i-1,j])
                else:
                    cumulativeEnergyMap[i][j] = mapTranspose[i][j] + min(cumulativeEnergyMap[i-1,j-1], cumulativeEnergyMap[i-1,j], cumulativeEnergyMap[i-1,j+1])
        cumulativeEnergyMap = cumulativeEnergyMap.transpose()
    return cumulativeEnergyMap



def find_optimal_vertical_seam(cumulativeEnergyMap):
    """
    Finds the least connected vertical seam using a vertical cumulative minimum energy map.

    Input: Vertical cumulative minimum energy map.
    Output:
        verticalSeam: vector containing column indices of the pixels in making up the seam.

    """

    verticalSeam = [0]*cumulativeEnergyMap.shape[0]

    ##########################################################################
    # TODO: Find the minimal connected vertical seam using the input         #
    # cumulative minimum energy map.                                         #
    ##########################################################################
    #verticalSeam = verticalSeam.tolist()
    #verticalSeam = list(verticalSeam)
    #cumulativeEnergyMap = cumulativeEnergyMap.tolist()

    lastIndex = len(cumulativeEnergyMap) - 1
    smallest_Index = np.argmin(cumulativeEnergyMap[lastIndex])
    verticalSeam[lastIndex] = smallest_Index

    cMap = cumulativeEnergyMap
    height, width = np.shape(cMap)
    verticalSeam[0] = np.argmin(cMap[height-1])

    i = lastIndex - 1
    j = smallest_Index
    if (height == 1):
        return verticalSeam
    while (i >= 0):
        #print(cMap[i][j])
        if (verticalSeam[i+1] == 0):
            tempList = [1000] * cumulativeEnergyMap[i].shape[0]
            tempList[j] = cumulativeEnergyMap[i][j]
            tempList[j+1] = cumulativeEnergyMap[i][j+1]
            verticalSeam[i] = np.argmin(tempList)
        elif (verticalSeam[i+1] == len(cumulativeEnergyMap[0]) - 1):
            #print("Here")
            tempList = [1000] * cumulativeEnergyMap[i].shape[0]
            tempList[j-1] = cumulativeEnergyMap[i][j-1]
            tempList[j] = cumulativeEnergyMap[i][j]
            verticalSeam[i] = np.argmin(tempList)
        else:
            #print("Here2")
            tempList = [1000] * cumulativeEnergyMap[i].shape[0]
            tempList[j-1] = cumulativeEnergyMap[i][j-1]
            tempList[j] = cumulativeEnergyMap[i][j]
            tempList[j+1] = cumulativeEnergyMap[i][j+1]
            verticalSeam[i] = np.argmin(tempList)
        j = verticalSeam[i]
        i -= 1

    return verticalSeam

def find_optimal_horizontal_seam(cumulativeEnergyMap):
    """
    Finds the least connected horizontal seam using a horizontal cumulative minimum energy map.

    Input: Horizontal cumulative minimum energy map.
    Output:
        horizontalSeam: vector containing row indices of the pixels in making up the seam.

    """
    horizontalSeam = [0]*cumulativeEnergyMap.shape[1]

    ##########################################################################
    # TODO: Find the minimal connected horizontal seam using the input       #
    # cumulative minimum energy map.                                         #
    ##########################################################################

    vertMap = cumulativeEnergyMap.transpose()
    horizontalSeam = find_optimal_vertical_seam(vertMap)
    cumulativeEnergyMap = cumulativeEnergyMap.transpose()

    '''
    lastIndex = len(cumulativeEnergyMap[0]) - 1
    smallest_Index = (np.argmin(cumulativeEnergyMap[:,lastIndex]))
    horizontalSeam[lastIndex] = smallest_Index

    i = lastIndex
    j = smallest_Index
    while (i > 0):
        rowLength = len(cumulativeEnergyMap)
        if (i == rowLength - 1):
            tempList = [300] * cumulativeEnergyMap.shape[0]

            #print(np.minimum(cumulativeEnergyMap[i-1][j-1],cumulativeEnergyMap[i-1][j]))
            #result = np.where(cumulativeEnergyMap[i-1] == np.minimum(cumulativeEnergyMap[i-1][j-1],cumulativeEnergyMap[i-1][j]))
            tempList[j-1] = cumulativeEnergyMap[j-1][i-1]
            tempList[j] = cumulativeEnergyMap[j][i-1]
            horizontalSeam[i-1] = np.argmin(tempList)
        elif (i == 0):
            #result = np.where(cumulativeEnergyMap[i-1] == np.minimum(cumulativeEnergyMap[i-1][j],cumulativeEnergyMap[i-1][j+1]))
            tempList = [300] * cumulativeEnergyMap.shape[0]
            tempList[j] = cumulativeEnergyMap[j][i-1]
            tempList[j+1] = cumulativeEnergyMap[j+1][i-1]
            horizontalSeam[i-1] = np.argmin(tempList)
        else:
            #result1 = np.minimum(cumulativeEnergyMap[i-1][j-1],cumulativeEnergyMap[i-1][j])
            #result = np.where(cumulativeEnergyMap[i-1] == np.minimum(result1, cumulativeEnergyMap[i-1][j+1]))
            tempList = [300] * cumulativeEnergyMap.shape[0]
            tempList[j-1] = cumulativeEnergyMap[j-1][i-1]
            tempList[j] = cumulativeEnergyMap[j][i-1]
            tempList[j+1] = cumulativeEnergyMap[j+1][i-1]
            horizontalSeam[i-1] = np.argmin(tempList)

        j = horizontalSeam[i-1]
        i -= 1
    '''
    return horizontalSeam

def reduce_width(img, energyImage):
    """
    Removes pixels along a seam, reducing the width of the input image by 1 pixel.

    Inputs:
        img: RGB image of shape (H x W x 3) from which a seam is to be removed.
        energyImage: The energy image of the input image.

    Outputs:
        reducedColorImage: The input image whose width has been reduced by 1 pixel
        reducedEnergyImage: The energy image whose width has been reduced by 1 pixel
    """
    reducedEnergyImageSize = (energyImage.shape[0], energyImage.shape[1] - 1)
    reducedColorImageSize = (img.shape[0], img.shape[1] - 1, 3)
    #print(reducedEnergyImageSize, reducedColorImageSize)

    reducedColorImage = np.zeros(reducedColorImageSize)
    reducedEnergyImage = np.zeros(reducedEnergyImageSize)

    minMap = cumulative_minimum_energy_map(energyImage, 'VERTICAL')
    bestVertSeam = find_optimal_vertical_seam(minMap)


    height = img.shape[0]
    width = img.shape[1]
    for i in range(height):
        reducedColorImage[i,:,:] = np.delete(img[i,:,:], bestVertSeam[i], axis = 0)
    reducedColorImage = reducedColorImage.astype(int)

    b = []
    for j in range(len(energyImage)):
        b.append(np.delete(energyImage[j],bestVertSeam[j]))
    reducedEnergyImage = np.asarray(b)

    #print("Done")
    #print(reducedColorImage)
    ##########################################################################
    # TODO: Compute the cumulative minimum energy map and find the minimal   #
    # connected vertical seam. Then, remove the pixels along this seam.      #
    ##########################################################################

    return reducedColorImage, reducedEnergyImage

def reduce_height(img, energyImage):
    """
    Removes pixels along a seam, reducing the height of the input image by 1 pixel.

    Inputs:
        img: RGB image of shape (H x W x 3) from which a seam is to be removed.
        energyImage: The energy image of the input image.

    Outputs:
        reducedColorImage: The input image whose height has been reduced by 1 pixel
        reducedEnergyImage: The energy image whose height has been reduced by 1 pixel
    """
    #print("aksdlj")
    reducedEnergyImageSize = tuple((energyImage.shape[0] - 1, energyImage.shape[1]))
    reducedColorImageSize = tuple((img.shape[0] - 1, img.shape[1], 3))

    reducedColorImage = np.zeros(reducedColorImageSize)
    reducedEnergyImage = np.zeros(reducedEnergyImageSize)


    minMap = cumulative_minimum_energy_map(energyImage, 'HORIZONTAL')
    bestHorzSeam = find_optimal_horizontal_seam(minMap)

    height = img.shape[0]
    width = img.shape[1]

    for i in range(width):
        reducedColorImage[:,i,:] = np.delete(img[:,i,:], bestHorzSeam[i], axis = 0)
    reducedColorImage = reducedColorImage.astype(int)

    b = []
    energyImage = energyImage.transpose()
    for j in range(len(energyImage)):
        b.append(np.delete(energyImage[j],bestHorzSeam[j]))
    reducedEnergyImage = np.asarray(b)
    reducedEnergyImage = reducedEnergyImage.transpose()
    ##########################################################################
    # TODO: Compute the cumulative minimum energy map and find the minimal   #
    # connected horizontal seam. Then, remove the pixels along this seam.    #
    ##########################################################################
    #b = []


    return reducedColorImage, reducedEnergyImage

def seam_carving_reduce_width(img, reduceBy):
    """
    Reduces the width of the input image by the number pixels passed in reduceBy.

    Inputs:
        img: Input image of shape (H x W X 3)
        reduceBy: Positive non-zero integer indicating the number of pixels the width
        should be reduced by.

    Output:
        reducedColorImage: The result of removing reduceBy number of vertical seams.
    """

    reducedColorImage = img[:, reduceBy//2:-reduceBy//2, :]  #crops the image

    ##########################################################################
    # TODO: For the Prague image, write a few lines of code to call the      #
    # we have written to find and remove 100 vertical seams                  #
    ##########################################################################
    energyImage = energy_image(img)
    for i in range(reduceBy):
        img, energyImage = reduce_width(img, energyImage)

    reducedColorImage = img
    return reducedColorImage

def seam_carving_reduce_height(img, reduceBy):
    """
    Reduces the height of the input image by the number pixels passed in reduceBy.

    Inputs:
        img: Input image of shape (H x W X 3)
        reduceBy: Positive non-zero integer indicating the number of pixels the
        height should be reduced by.

    Output:
        reducedColorImage: The result of removing reduceBy number of horizontal
        seams.
    """

    reducedColorImage = img[reduceBy//2:-reduceBy//2, :, :]  #crops the image

    ##########################################################################
    # TODO: For the Prague image, write a few lines of code to call the      #
    # we have written to find and remove 100 horizontal seams.               #
    ##########################################################################
    energyImage = energy_image(img)
    for i in range(reduceBy):
        print(i)
        img, energyImage = reduce_height(img, energyImage)

    reducedColorImage = img

    return reducedColorImage

from PIL import Image
img = Image.open("C:/Users/aksha/Human in the Loop DA/Project Files/MountEverest.jpgN")

img = img.convert('RGB')
#rgb_im = im.convert('RGB')
myArr = np.asarray(img)
print(myArr.shape)

originalImage = Image.fromarray(myArr)
originalImage.show()


#newArr = seam_carving_reduce_width(myArr, 150)
#newImage = Image.fromarray((newArr).astype(np.uint8))
print(newArr.shape)
newImage.show()

print("Done")
#plt.plot(newArr)
#plt.title("Shrunk Image")