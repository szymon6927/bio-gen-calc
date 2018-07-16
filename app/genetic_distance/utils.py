import numpy as np
import itertools
from math import sqrt, log
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from io import BytesIO
import base64


class GeneticDistance:

    def __init__(self, data):
        self.data = data
        self.distances = []  # helper list for building correct matrix
        self.matrix = []
        self.condensed_matrix = []
        self.column_range = int(self.data["taxon_number"])

    def estimate_J(self):
        sum_of_square = {}
        for i in range(self.column_range):
            sum_all = sum(j * j for j in self.data["column_" + str(i)]) / int(self.data["locus_number"])
            sum_of_square["j_" + str(i)] = round(sum_all, 5)

        return sum_of_square

    def calcuate_x_y(self):
        sum_product = {}
        pair_combination = list(itertools.combinations(range(self.column_range), 2))
        for pair in pair_combination:
            product = [a * b for a, b in zip(self.data["column_" + str(pair[0])], self.data["column_" + str(pair[1])])]

            key = f'{pair[0]}_{pair[1]}'
            sum_product[key] = round(sum(i for i in product) / int(self.data["locus_number"]), 5)

        return sum_product

    def calcuate_distances(self):
        pair_combination = list(itertools.combinations(range(self.column_range), 2))

        sum_of_square = self.estimate_J()
        sum_product = self.calcuate_x_y()

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'
            sum_one = sum_of_square[f'j_{pair[0]}']
            sum_two = sum_of_square[f'j_{pair[1]}']
            i = sum_product[key] / sqrt(sum_one * sum_two)
            i_log = -1 * log(i)
            self.distances.append(round(i_log, 5))

        self.condensed_matrix = self.distances[:]

    def build_matrix(self, end=None):
        if end is None:
            end = self.column_range - 1
            
        if end == 0:
            self.matrix_conversion()
            return

        temp = []
        for i in range(end):
            try:
                temp.append(self.distances[i])
            except IndexError:
                print("IndexError")

            if i == end:
                break

        del self.distances[:end]  # delete first n elem

        zeros_list = [0] * (self.column_range - 1 - len(temp))
        zeros_list += temp  # add to zeros_list bcs zeros must be at begining
        self.matrix.append(zeros_list)
        self.build_matrix(end - 1)

    def matrix_conversion(self):
        """
        matrix re-build, prepare for displaying dendrograms
        """
        matrix_tuple = self.convert_to_tuple()
        conversion = np.column_stack(matrix_tuple)
        self.matrix = conversion

    def convert_to_tuple(self):
        nested_lst_of_tuples = [tuple(l) for l in self.matrix]

        return tuple(nested_lst_of_tuples)

    def redner_matrix(self):
        """Returns a LaTeX bmatrix

        :a: numpy array
        :returns: LaTeX bmatrix as a string
        """
        if len(self.matrix.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(self.matrix).replace('[', '').replace(']', '').splitlines()
        rv = [r'\begin{bmatrix}']
        rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        rv += [r'\end{bmatrix}']
        return '\n'.join(rv)

    def render_dendrogram(self):
        mathod_linkage = linkage(self.condensed_matrix, 'average')

        dendro = dendrogram(mathod_linkage, orientation='left')

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = figfile.getvalue()  # extract string (stream of bytes)
        figdata_png = base64.b64encode(figdata_png)

        decoded = figdata_png.decode("utf-8")
        return decoded
