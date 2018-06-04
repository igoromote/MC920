import numpy as np
import cv2
import math
import sys
import argparse

def interpolationByNearetNeighbor(x,y):
    return int(round(x)), int(round(y))

def interpolationBilinear(x,y, image):
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    return (1 - dx) * (1 - dy) * image[math.floor(x)][math.floor(y)] + dx * (1 - dy) * image[math.floor(x) + 1][math.floor(y)] + (1 - dx) * dy * image[math.floor(x)][math.floor(y) + 1] + dx * dy * image[math.floor(x) + 1][math.floor(y) + 1]

def interpolationBicubic(x, y, image):
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    #tratamento se nao eh borda e pa
    def P(t):
        if (t > 0):
            return t
        else:
            return 0

    def R(s):
        return (1/6)*(P(s+2)^3 - 4*P(s+1)^3 + 6*P(s)^3 - 4 * P(s-1)^3)

    m = -1
    n = -1
    accumulator = 0
    while (m <= 2):
        while (n <= 2):
            accumulator = image[math.floor(x)][math.floor(y)]*R(m - dx)*R(dy - n)
            n = n + 1
        m = m + 1
    return accumulator

def interpolationByLagrange(x, y, image):
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    def L(n):
        first = (-dx * (dx - 1) * (dx - 2) * image[math.floor(x) - 1][math.floor(y) + n - 2])/6
        second = ((dx + 1) * (dx - 1) * (dx - 2) * image[math.floor(x)][math.floor(y) + n - 2])/2
        third = (-dx * (dx + 1) * (dx - 2) * image[math.floor(x) + 1][math.floor(y) + n - 2])/2
        forth = (dx * (dx + 1) * (dx - 1) * image[math.floor(x) + 2][math.floor(y) + n - 2])/6
        return first + second + third + forth
    firstTerm = (-dy * (dy - 1) * (dy - 2) * L(1))/6
    secondTerm = ((dy + 1) * (dy - 1) * (dy - 2) * L(2))/2
    thirdTerm = (-dy * (dy + 1) * (dy - 2) * L(3))/2
    forthTerm = (dy * (dy + 1) * (dy - 1) * L(4))/6
    return firstTerm + secondTerm + thirdTerm + forthTerm

def treatParse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--angle", dest = "angle", default = "0", help="Rotate angle", type=float)
    parser.add_argument("-e", "--scaleFactor", dest = "scale", default = "1.0", help="Scale factor", type=float)
    parser.add_argument("-d", "--outputDimension",dest ="dim", help="Width and Height for output image", nargs=2, type=int)
    parser.add_argument("-m", "--interpolationMethod",dest = "method", help="Interpolation Method", type=int)
    parser.add_argument("-i", "--inputName",dest = "input", help="Input link")
    parser.add_argument("-o", "--ouputName",dest = "output", help="Output Name")
    args=parser.parse_args()
    return args

def checkArgs (args):
    if (args.angle != 0 and args.scale != 1.0):
        return 0
    if (args.angle != 0):
        return 1
    if (args.scale != 1.0):
        return 2
    return -1

def handleCheckArgs(i, args):
    if (i == 0):
        print("Choose only one: change scale or rotate")
        exit(1)
    if (i == -1):
        print("Parameters won't change sacle neither rotate")
        exit(1)
    if (i == 1):
        print("Hey")
    if (i == 2):
        changeScale(args)

def filterEmptyPixels(img, width, height):
    img2 = np.empty((width, height))
    for i in range (0, width):
        for j in range (0, height):
            if (img[i][j] == 0):
                count1 = 0
                count2 = 0
                for iMax in range(-1, 2):
                    for jMax in range(-1, 2):
                        try:
                            if (img[i + iMax][j + jMax] != 0):
                                count1 += img[i + iMax][j + jMax]
                                count2 += 1
                        except:
                            count1 = count1
                img2[i][j] = int(count1/count2)
            else:
                img2[i][j] = img[i][j]
        img2 = img2.astype(np.uint8)
    return img2

def changeScale(args):
    img = cv2.imread(args.input, 0)
    width = img.shape[0]
    height = img.shape[1]
    numBorder = 0
    newWidth = int(round(width/args.scale, 0))
    newHeight = int(round(height/args.scale, 0))
    newImage = np.zeros((newWidth, newHeight))
    for i in range (0, width):
        for j in range(0, height):
            k = int(round(1/args.scale, 0))
            x, y = interpolationByNearetNeighbor(i/args.scale, j/args.scale)
            try:
                for iScale in range (0 , max(1, k)):
                    for jScale in range (0 , max(1, k)):
                        newImage[x + iScale][y + jScale] = int(img[i][j])
            except:
                numBorder = numBorder + 1
    newImage1 = newImage.astype(np.uint8)
    print(str(width)+ " " + str(height)+ " ")
    print(str(newWidth)+ " " + str(newHeight)+ " ")
    cv2.imshow( "Display window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow( "Display window", newImage1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    newImage2 = filterEmptyPixels(newImage1, newWidth, newHeight)
    cv2.imshow( "Display window", newImage2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    args = treatParse()
    i = checkArgs (args)
    handleCheckArgs(i, args)

    # if (dx < 0.5 and dy < 0.5):
    #     return floor(x), floor(y)
    # elif (dx >= 0.5 and dy < 0.5):
    #     return ceil(x), floor(y)
    # elif (dx < 0.5 and dy >= 0.5):
    #     return floor(x), ceil(y)
    # elif (dx >= 0.5 and dy >= 0.5):
    #     return ceil(x), ceil(y)
