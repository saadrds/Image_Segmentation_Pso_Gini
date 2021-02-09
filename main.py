# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import *
import numpy as np
import cv2
import math
import gini_entropy

im_gray = cv2.imread("sources/butterfly.jpg", cv2.IMREAD_GRAYSCALE)

imageTest = [[122, 233, 213], [112, 33, 32], [13, 41, 24]]
matrix1 = [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
imageTest2 = [[121, 232, 223], [112, 13, 32], [33, 42, 64]]

colors = []
colors += [[0, 0, 255]]  # red
colors += [[255, 0, 0]]  # blue
colors += [[0, 255, 0]]  # green
colors += [[0, 255, 255]]  # yellow
colors += [[0, 128, 255]]  # orange
colors += [[255,149,0]]


def draw_image(image, tab):
    nb_lines = len(image)
    nb_col = len(image[0])
    colored_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for k in range(1, len(tab)):
        for i in range(len(image)):
            for j in range(len(image[0])):
                if tab[k - 1] < image[i][j] <= tab[k]:
                    colored_image[i][j] = colors[k]
    new_image = np.array(colored_image)
    cv2.imshow("image segmentée tata !", colored_image)
    cv2.waitKey()


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
            if image[i][j] > gray_max:
                gray_max = image[i][j]
            if image[i][j] < gray_min:
                gray_min = image[i][j]

    position_tab = [[randint(gray_min, gray_max) for i in range(nb_seuil)] for j in range(50)]
    best_position_tab = []
    velocity_tab = [[0.0 for i in range(nb_seuil)] for j in range(50)]
    g_best_tab = []
    for element in position_tab:
        best_position_tab += [element]
        g_best_tab += [element]

    # initialisation ended

    # define an shortcut for gini_entropy
    def ge(pixel_tab):
        return gini_entropy.gini_entropy(image, pixel_tab, gray_min, gray_max)

    # function that finds the best position in the whole swarm
    def g_best_finder(ptab, indice):
        neighbours = []
        # collect the neighbours of the particle i j
        for k in range(indice - 1, indice + 2):
            if k not in (-1, len(ptab)):
                neighbours += [ptab[k]]
        # looking for g_best in the population
        gbest = neighbours[0]
        for el in neighbours:
            if ge(gbest) < ge(element):
                gbest = element
        return el

    # find the g best initation
    g_best = best_position_tab[0]
    for i in range(1, len(best_position_tab)):
        if ge(best_position_tab[i]) < ge(g_best):
            g_best = best_position_tab[i]
    # algorithm  iterations:

    k = 0  # iteration init on 0
    psnr_value = 0

    # do until psnr index is above 30db or we did a lot of iteration to avoid infinity loop
    for k in range(5):
        # psnr_value = psnr(image, best_position_tab)
        for i in range(nb_col):
            #  g_best_tab[i] = g_best_finder(position_tab, i)  # find g_best around the particle i,j
            w = 2 / abs(2 - phi - math.sqrt(phi * (phi - 4)))  # calculating the inert
            c1 = phi1 * w  # calculating momentum coefficient 1
            c2 = phi2 * w  # calculating momentum coefficient 2
            # calculate new velocity
            for j in range(nb_seuil):
                velocity_tab[i][j] = w * velocity_tab[i][j] + (
                        c1 * random() * (best_position_tab[i][j] - position_tab[i][j])) + (
                                             c2 * random() * (g_best[j] - position_tab[i][j]))
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
                        position_tab[i][j] = position_tab[i][j+1] /2
                    elif position_tab[i][j] < gray_min:  # test if it's below the gray_min
                        position_tab[i][j] = gray_min
                # test if this is the last seuil
                elif j == nb_seuil - 1:
                    if position_tab[i][j] <= position_tab[i][j - 1]:  # test if it's below previous seuil
                        position_tab[i][j] = (position_tab[i][j - 1] + gray_max)/2
                    elif position_tab[i][j] > gray_max:  # test if it's above the gray_max
                        position_tab[i][j] = gray_max
                # if it's seuil in the middle of the particle we test if it's between the previous and the next sueil
                else:
                    position_tab[i][j] = (position_tab[i][j-1] + position_tab[i][j+1]) /2

            # update the new personal best position
            if ge(position_tab[i]) < ge(best_position_tab[i]):
                best_position_tab[i] = position_tab[i]
                # update the new g_best position if the personal best position is better than g_best
                if ge(best_position_tab[i]) < ge(g_best_tab[i]):
                    g_best = best_position_tab[i]

        print(k)
    # we pick the optimum solution from the gbest tab
    optimum = [gray_min] + g_best + [gray_max]
    print(optimum)
    draw_image(image, optimum)
    # algorithm ended
    print(k)
    print("optimum : ", optimum)

    # new_image = numpy.array(best_position_tab)
    # cv2.imshow("image", new_image)
    # cv2.waitKey()


pso(im_gray, 4)

