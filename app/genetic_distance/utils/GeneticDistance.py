# important for use matplotlib at backend
import os
import matplotlib as mpl

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from io import BytesIO
import base64


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
            'complete-linkage': 'complete'
        }

        distance = self.data.get("type_of_dendrogram")
        if distance is None:
            return dendro_method["upgma"]

        return dendro_method[distance]

    def redner_matrix(self):
        """Returns a LaTeX bmatrix

        :a: numpy array
        :returns: LaTeX bmatrix as a string
        """

        # now only for test
        self.matrix = squareform(self.condensed_matrix)
        print(self.matrix, flush=True)

        index = [i for i in range(0, self.column_range + 1)]
        columns = [i for i in range(0, self.column_range + 1)]

        result = pd.DataFrame(data=self.matrix)

        # if len(self.matrix.shape) > 2:
        #     raise ValueError('bmatrix can at most display two dimensions')
        # lines = str(self.matrix).replace('[', '').replace(']', '').replace('0.', ',').splitlines()
        # rv = [r'\begin{bmatrix}']
        # rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
        # rv += [r'\end{bmatrix}']
        # return '\n'.join(rv)
        return result.to_html()

    def render_dendrogram(self):
        method = linkage(self.condensed_matrix, self.detect_dendrogram_type())

        dendro = dendrogram(method, orientation='left')

        figfile = BytesIO()
        plt.savefig(figfile, format='png', dpi=120)
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = figfile.getvalue()  # extract string (stream of bytes)
        figdata_png = base64.b64encode(figdata_png)
        decoded = figdata_png.decode("utf-8")
        plt.clf()

        return decoded
