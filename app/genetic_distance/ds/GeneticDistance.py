# important for use matplotlib at backend
import base64
import itertools
import os
from io import BytesIO

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')


class GeneticDistance:
    def __init__(self, data):
        self.data = data
        self.distances = []  # helper list for building correct matrix
        self.matrix = []
        self.condensed_matrix = []
        self.column_range = int(self.data["taxon_number"])

    def get_pair_combination(self, size):
        """
        :param size:
        :return: list of 2-length tuples of combination from size
        """
        return list(itertools.combinations(range(size), 2))

    def get_condensed_matrix(self):
        return self.condensed_matrix

    def get_matrix(self):
        return self.matrix

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

    def detect_dendrogram_type(self):
        dendro_method = {
            'upgma': 'average',
            'wpgma': 'weighted',
            'upgmc': 'centroid',
            'wpgmc': 'median',
            'single-linkage': 'single',
            'complete-linkage': 'complete',
        }

        distance = self.data.get("type_of_dendrogram")
        if distance is None:
            return dendro_method["upgma"]

        return dendro_method[distance]

    def render_matrix(self):
        """Returns a LaTeX bmatrix

        :a: numpy array
        :returns: LaTeX bmatrix as a string
        """

        # now only for test
        self.matrix = squareform(np.asarray(self.condensed_matrix))

        result = pd.DataFrame(data=self.matrix)

        return result.to_html()

    def render_dendrogram(self):
        method = linkage(np.asarray(self.condensed_matrix), self.detect_dendrogram_type())

        dendrogram(method, orientation='left')

        figfile = BytesIO()
        plt.savefig(figfile, format='png', dpi=120)
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = figfile.getvalue()  # extract string (stream of bytes)
        figdata_png = base64.b64encode(figdata_png)
        decoded = figdata_png.decode("utf-8")
        plt.clf()

        return decoded
