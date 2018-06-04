# Projeto 3 - Alinhamento de Documentos
# MC920 - Introducao ao Processamento Digital de Imagem
# RA169819 - Igor Mateus Omote

import sys
import numpy as np
from PIL import Image as im
from PIL import ImageFilter
from scipy.ndimage import interpolation
from scipy import ndimage
import time
import cv2
import math


# Rotate image, then calculate histogram and sum the module of diference between two consecutive lines,
# The max diference of this sum's will be the optimal angle
def difBetweenLine(img, angle):
    # 'order' parameter was chosen equal 0 so optimize time
    rotated = interpolation.rotate(img, angle, order=0)
    histogram = np.sum(rotated, axis=1)
    diference = np.sum(abs((histogram[1:] - histogram[:-1])))
    return diference

# Count number of lines with at least 1 black dot, the minimal number of lines is the optimal angle
# However, is subject to noise, and we won't use
def countLines(histogram, height):
    count = 0
    for line in height:
        if histogram[line] > 0:
            count = count + 1
    return count

# Find which angle (between -45 and 45) has the value, if did't find, return -1
def findIndex(array, value):
    i = - 45
    while i < 46:
        if array[i] == value:
            return i
        i = i + 1
    return -100

def byAngle(imgLink, outputName):

    # Open image
    img = im.open(imgLink)
    # Dimensions of img
    width, height = img.size
    # Convert img to a array, then to a Matrix
    imgArray = np.array(img.convert('1').getdata())
    imgMatrix = (imgArray.reshape(height, width) / 255.0)
    # Create a matrix with pixels switched to avoid noise
    imgInvert = 1 - imgMatrix

    # We'll try angles belong to [-45,45], with gap == 1
    angles = np.arange(-45, 46, 1)
    diferences = []
    for angle in angles:
        diference = difBetweenLine(imgInvert, angle)
        diferences.append(diference)

    # The biggest diference is the best angle
    toAngle = max(diferences)
    i = findIndex (diferences, toAngle)

    if i != -100:
        rotationAngle = angles[i]
    else:
        print ("Error")
        exit(1)

    print ('Best angle is: ', rotationAngle)

    # Rotate original image with angle found
    data = interpolation.rotate(imgMatrix, rotationAngle, order=5)
    # To save a image must be converted to RGB
    img = im.fromarray(255 * data).convert('RGB')
    # Function used have some noise, so we'll use a Median Filter to adjust
    img.filter(ImageFilter.MedianFilter)
    # Save image with name from input
    img.save(outputName)

def byHough(imgLink, outputName):

    img = cv2.imread(imgLink, 0)

    width = img.shape[0]
    height = img.shape[1]

    # Edge detector Canny
    img_edges = cv2.Canny(img, 100, 100, apertureSize=3)

    # Operate Hough
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)

    # save all line's angle in a array
    angles = []
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img_edges, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # The most frequent angle is the best angle
    median_angle = np.median(angles)
    print ("Best angle by Canny is: ",median_angle)

    # Rotate original image with angle found
    img = ndimage.rotate(img, median_angle)
    # Save image with nam from input
    cv2.imwrite(outputName, img)


# Initiate
if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print('Invalid number of args! The correct input is: python alinhar.py <input_image.png> <1 == Projection, 2 == Hough> <output_image.png>')
        exit(1)

    input = sys.argv[1]
    mode = sys.argv[2]
    output = sys.argv[3]

    if (int(mode) == 1):
        byAngle(input, output)
    elif (int(mode) == 2):
        byHough(input, output)
    else:
        print('Invalid mode! The correct input is: python alinhar.py <input_image.png> <1 == Projection, 2 == Hough> <output_image.png>')
