# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import *
# import numpy
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
def g_best_finder(image, i):
    neighbours = []
    # collect the neighbours of the particle i j
    for k in range(i - 1, i + 2):
        if k not in (-1, len(image)):
            neighbours += [image[k]]
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


def pso(image, nb_region):
    # variables and parameters initialisations
    nb_seuil = nb_region - 1
    nb_col = 50
    w = 0.9
    phi1 = 2
    phi2 = 2.05
    phi = phi1 + phi2
    # initialisation of matrix positions and velocity (search space)
    gray_max = 0
    gray_min = 255
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[0][0] > gray_max:
                gray_max = image[0][0]
            if image[0][0] < gray_min:
                gray_min = image[0][0]

    position_tab = [[randint(gray_min, gray_max) for i in range(nb_seuil)] for j in range(50)]
    best_position_tab = [[position_tab[i][j] for i in range(nb_seuil)] for j in range(nb_col)]
    velocity_tab = [[0.0 for i in range(nb_seuil)] for j in range(nb_col)]
    g_best_tab = [[position_tab[i][j] for i in range(nb_seuil)] for j in range(nb_col)]

    # initialisation ended

    # algorithm  iterations:

    k = 0  # iteration init on 0
    psnr_value = 0

    # do until psnr index is above 30db or we did a lot of iteration to avoid infinity loop
    for k in range(20):
        if k > 0:
            psnr_value = psnr(image, best_position_tab)

        for i in range(nb_col):
            g_best_tab[i] = g_best_finder(image, i)  # find g_best around the particle i,j
            w = 2 / abs(2 - phi - math.sqrt(phi * (phi - 4)))  # calculating the inert
            c1 = phi1 * w  # calculating momentum coefficient 1
            c2 = phi2 * w  # calculating momentum coefficient 2

            # calculate new velocity
            for j in range(nb_seuil):
                velocity_tab[i][j] = w * velocity_tab[i][j] + (
                        c1 * random() * (best_position_tab[i][j] - position_tab[i][j])) + (
                                             c2 * random() * (g_best_tab[i][j] - position_tab[i][j]))
                if velocity_tab[i][j] > 3:  # test if the velocity limit is beyond 3
                    velocity_tab[i][j] = 3
                elif velocity_tab[i][j] < -3:  # test if the velocity limit is below -3
                    velocity_tab[i][j] = -3

                # calculate new position
                position_tab[i][j] += velocity_tab[i][j]
            # now checking if the position is in the good borders

                # test if this is the first seuil
                if j == 0:
                    if position_tab[i][j] >= position_tab[i][j + 1]:  # test if its above the next seuil
                        position_tab[i][j] = position_tab[i][j] - 1
                    elif position_tab[i][j] < gray_min:  # test if it's below the gray_min
                        position_tab[i][j] = gray_min
                # test if this is the last seuil
                elif j == nb_seuil - 1:
                    if position_tab[i][j] <= position_tab[i][j - 1]:  # test if it's below previous seuil
                        position_tab[i][j] = position_tab[i][j - 1] + 1
                    elif position_tab[i][j] > gray_max:  # test if it's above the gray_max
                        position_tab[i][j] = gray_max
                # if it's seuil in the middle of the particle we test if it's between the previous and the next sueil
                else:
                    if position_tab[i][j] >= position_tab[i][j + 1]:
                        position_tab[i][j] = position_tab[i][j] - 1
                    elif position_tab[i][j] <= position_tab[i][j - 1]:
                        position_tab[i][j] = position_tab[i][j - 1] + 1

            # update the new personal best position
            if ge(position_tab[i]) < ge(best_position_tab[i]):
                best_position_tab[i] = position_tab[i]
                # update the new g_best position if the personal best position is better than g_best
                if ge(best_position_tab[i]) < ge(g_best_tab[i]):
                    g_best_tab[i] = best_position_tab[i]

        k = k + 1
    # we pick the optimum solution from the gbest tab
    optimum = g_best_tab[0]
    optimum_line = 0
    for i in range(nb_col):
        if g_best_tab[i] < optimum:
            optimum = g_best_tab[i]
            optimum_line = i
    # algorithm ended
    print(k)
    print("optimum : ", optimum)
    print("index : ", optimum_line)
    # new_image = numpy.array(best_position_tab)
    # cv2.imshow("image", new_image)
    # cv2.waitKey()


pso(im_gray, 5)
