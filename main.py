# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import *
import numpy
import cv2
import math

im_gray = cv2.imread("sources/Cameraman256.png", cv2.IMREAD_GRAYSCALE)

imageTest = [[122, 233, 213], [112, 33, 32], [13, 41, 24]]
matrix1 = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
imageTest2 = [[121, 232, 223], [112, 13, 32], [33, 42, 64]]


# gini entropy function
def ge(num):
    return num


# function that finds the best position in the whole swarm
def g_best_finder(image, i, j):
    neighbours = []
    # collect the neighbours of the particle i j
    for k in range(i - 1, i + 2):
        for m in range(j - 1, j + 2):
            if k not in (-1, len(image)) and m not in (-1, len(image[0])) and not (k == i and m == j):
                neighbours += [image[k][m]]
    # looking for g_best in the population
    gbest = neighbours[0]
    element = 0
    for element in neighbours:
        if ge(gbest) < ge(element):
            gbest = element
    return element


# psnr function (peak signal to noise ratio)
def psnr(initial_image, end_image):
    mse = 0  # mean square error
    m = len(initial_image)
    n = len(initial_image[0])
    for i in range(m):
        for j in range(n):
            mse += pow(initial_image[i][j] - end_image[i][j], 2)
    mse = mse / (m * n)
    if mse == 0:
        return 0
    return 20 * math.log10(255) - 10 * math.log10(mse)  # psnr value


def pso(image):
    # variables and parameters initialisations
    w = 0.9
    c1 = 2
    c2 = 2.05
    # initialisation of matrix positions and velocity (search space)
    nb_lines = len(image)
    nb_col = len(image[0])
    position_tab = [[0.0 for i in range(nb_lines)] for j in range(nb_col)]
    best_position_tab = [[0.0 for i in range(nb_lines)] for j in range(nb_col)]
    velocity_tab = [[0.0 for i in range(nb_lines)] for j in range(nb_col)]
    g_best_tab = [[0.0 for i in range(nb_lines)] for j in range(nb_col)]
    for i in range(nb_lines):
        for j in range(nb_col):
            position_tab[i][j] = image[i][j]
            best_position_tab[i][j] = image[i][j]
            g_best_tab[i][j] = image[i][j]
    # initialisation ended

    # algorithm  iterations:

    k = 0  # iteration init on 0
    psnr_value = 0

    # do until psnr index is above 30db or we did a lot of iteration to avoid infinity loop
    while k < 20:
        if k > 0:
            psnr_value = psnr(image, best_position_tab)
            print(psnr_value)
        for i in range(nb_lines):
            for j in range(nb_col):
                g_best_tab[i][j] = g_best_finder(image, i, j)  # find g_best around the particle i,j
                # calculate new velocity
                velocity_tab[i][j] = w * velocity_tab[i][j] + (
                        c1 * random() * (best_position_tab[i][j] - position_tab[i][j])) + (
                                             c2 * random() * (g_best_tab[i][j] - position_tab[i][j]))
                # calculate new position
                position_tab[i][j] += velocity_tab[i][j]

                # update the new personal best position
                if ge(position_tab[i][j]) < ge(best_position_tab[i][j]):
                    best_position_tab[i][j] = position_tab[i][j]
                    # update the new g_best position if the personal best position is better than g_best
                    if ge(best_position_tab[i][j]) < ge(g_best_tab[i][j]):
                        g_best_tab[i][j] = best_position_tab[i][j]

        k = k + 1
    # we pick the optimum solution from the gbest tab
    optimum = g_best_tab[0][0]
    optimum_line = 0
    optimum_cole = 0
    for i in range(nb_lines):
        for j in range(nb_col):
            if g_best_tab[i][j] < optimum:
                optimum = g_best_tab[i][j]
                optimum_line = i
                optimum_cole = j
    # algorithm ended
    print(k)
    print("optimum : ", optimum)
    print("index : ", optimum_line, ",", optimum_cole)
    new_image = numpy.array(best_position_tab)
    cv2.imshow("image", new_image)
    cv2.waitKey()


pso(im_gray)
