class Region:
    n: int  # number of pixel inside region
    f: float  # frequency of pixels in region
    f_cum: float  # cumulate frequency of pixels in region
    center: float  # centre of region
    gray_percent: float  # gray percent of region
    gray_percent_cum: float  # cumulate of gray centre in region
    l1: int  # min limit
    l2: int  # max limit
    pixel_tab: [int]

    # constructor with the region limits
    def __init__(self, l1, l2):
        self.pixel_tab = [l1]
        self.pixel_tab += [l2]

    def add_pixel(self, pixel):  # add pixel to tab
        self.pixel_tab += [pixel]

    # pixels adding completed
    def calculate_parameters(self, total_pixels):
        self.n = len(self.pixel_tab)
        self.pixel_tab = self.pixel_tab
        self.f = self.n / total_pixels
        self.l1 = self.pixel_tab[0]
        self.l2 = self.pixel_tab[self.n - 1]
        self.center = (self.l1 + self.l2) / self.n

    # f_cum calculation
    def f_cum_cal(self, f_cum_before):
        self.f_cum = f_cum_before + self.f
        return self.f_cum

    # centre calculation
    def gray_percent_cum_cal(self, gray_cum_before):
        self.gray_percent_cum = gray_cum_before + self.gray_percent


class Image:
    regions: [Region]  # regions tab
    nb_lines: int
    nb_columns: int

    def __int__(self, image_matrix, seuils, min_gray, max_gray):
        self.min = min_gray  # min gray value
        self.max = max_gray  # max gray value
        self.image_matrix = image_matrix  # image matrix
        self.nb_lines = len(image_matrix)
        self.nb_columns = len(image_matrix[0])
        # adding regions with limits of seuils
        self.regions = [Region(min, seuils[0])]
        for i in range(1, len(seuils)):
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
        for element in self.regions:
            # giving the total number of pixels to each region for calculating
            element.calculate_parameters(self.nb_lines * self.nb_columns)
