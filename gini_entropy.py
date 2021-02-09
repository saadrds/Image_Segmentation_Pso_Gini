import math


class Region:
    n: int  # number of pixel inside region
    f: float  # frequency of pixels in region
    # f_cum: float  # cumulate frequency of pixels in region
    centre: float  # centre of region
    gray_percent: float  # gray percent of region
    gray_percent_cum: float  # cumulate of gray centre in region
    l1: float  # min limit
    l2: float  # max limit
    width: float
    pixel_tab: []

    # constructor with the region limits
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
        self.width = l1 + l2
        self.pixel_tab = [l1]
        self.pixel_tab += [l2]

    def add_pixel(self, pixel):  # add pixel to tab
        self.pixel_tab.insert(1, pixel)

    # pixels adding completed
    def calculate_parameters(self, total_pixels):
        self.n = len(self.pixel_tab)
        self.pixel_tab = self.pixel_tab
        self.f = self.n / total_pixels
        self.centre = self.width / self.n

    # f_cum calculation
    """
    def f_cum_cal(self, f_cum_before):
        self.f_cum = f_cum_before + self.f
        return self.f_cum
    """

    # gray cumulative percent calculation by adding the value before as an argument
    def gray_percent_cum_cal(self, gray_cum_before):
        self.gray_percent_cum = gray_cum_before + self.gray_percent
        return self.gray_percent_cum


class Image:
    regions: []  # regions tab
    nb_lines: int
    nb_columns: int
    gini = 0
    entropy = 0

    def __init__(self, image_matrix, seuils, min_gray, max_gray):
        self.min = min_gray  # min gray value
        self.max = max_gray  # max gray value
        self.image_matrix = image_matrix  # image matrix
        self.nb_lines = len(image_matrix)
        self.nb_columns = len(image_matrix[0])
        # adding regions with limits of seuils
        self.regions = [Region(min_gray, seuils[0])]
        for i in range(len(seuils) - 1):
            self.regions += [Region(seuils[i], seuils[i + 1])]
        self.regions += [Region(seuils[len(seuils) - 1], self.max)]
        #  grouping pixels of image in propre regions
        for i in range(self.nb_lines):
            for j in range(self.nb_columns):
                # looking for the value of pixel in each region , if found then break
                for k in range(len(self.regions)):
                    if image_matrix[i][j] in (self.regions[k].l1, self.regions[k].l2):
                        self.regions[k].add_pixel(image_matrix[i][j])
                        break
        # calculating regions attributes
        # f_before = 0
        g_before = 0
        g2_before = 0
        gini = 0
        total_gray = 0
        for i in range(len(self.regions)):
            # giving the total number of pixels to each region for calculating
            self.regions[i].calculate_parameters(self.nb_lines * self.nb_columns)
            total_gray += self.regions[i].n * self.regions[i].centre
            #  f_before = self.regions[i].f_cum_cal(f_before)

        for i in range(len(self.regions)):
            self.entropy += self.regions[i].f * math.log10(self.regions[i].f)  # entropy index using p = f
            self.regions[i].gray_percent = (self.regions[i].n * self.regions[i].centre) / total_gray  # gray percent
            g2_before = self.regions[i].gray_percent_cum_cal(g_before)
            gini += self.regions[i].f * (g_before + self.regions[i].gray_percent_cum)  # gini calculation
            g_before = g2_before
        self.gini = 1 - gini


# definition of the fitness function
def gini_entropy(image_test, tab_pixel, min_gray, max_gray):
    # initialisation an image object with the image matrix and particle and the gray botder
    img1 = Image(image_test, tab_pixel, min_gray, max_gray)
    return img1.gini - img1.entropy
