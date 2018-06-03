import numpy as np
import cv2
import math

def interpolationByNearetNeighbor(x,y):
    return math.round(x), math.round(y)

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


    # if (dx < 0.5 and dy < 0.5):
    #     return floor(x), floor(y)
    # elif (dx >= 0.5 and dy < 0.5):
    #     return ceil(x), floor(y)
    # elif (dx < 0.5 and dy >= 0.5):
    #     return floor(x), ceil(y)
    # elif (dx >= 0.5 and dy >= 0.5):
    #     return ceil(x), ceil(y)
