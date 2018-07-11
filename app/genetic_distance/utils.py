import numpy as np
import itertools
from math import sqrt, log
from scipy.spatial import distance_matrix


class GeneticDistance:

    def __init__(self, data):
        self.data = data

    def estimate_J(self):
        sum_of_square = {}
        for i in range(int(self.data["taxon_number"])):
            sum_all = sum(j * j for j in self.data["column_" + str(i)]) / int(self.data["locus_number"])
            sum_of_square["j_" + str(i)] = round(sum_all, 5)

        print(f'sum_of_square: {sum_of_square}', flush=True)
        return sum_of_square

    def calcuate_x_y(self):
        sum_product = {}
        column_range = int(self.data["taxon_number"])
        pair_combination = list(itertools.combinations(range(column_range), 2))
        for pair in pair_combination:
            product = [a * b for a, b in zip(self.data["column_" + str(pair[0])], self.data["column_" + str(pair[1])])]

            key = f'{pair[0]}_{pair[1]}'
            sum_product[key] = round(sum(i for i in product) / int(self.data["locus_number"]), 5)

        print(f'sum_product: {sum_product}', flush=True)
        return sum_product

    def calcuate_distances(self):
        distances = []

        column_range = int(self.data["taxon_number"])
        pair_combination = list(itertools.combinations(range(column_range), 2))

        sum_of_square = self.estimate_J()
        sum_product = self.calcuate_x_y()

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'
            sum_one = sum_of_square[f'j_{pair[0]}']
            sum_two = sum_of_square[f'j_{pair[1]}']
            i = sum_product[key] / sqrt(sum_one * sum_two)
            i_log = -1 * log(i)
            distances.append(round(i_log, 5))

        print(f'matrix_of_distance: {matrix_of_distance}', flush=True)

        return distances


    def build_matrix(self):
        distances = self.calcuate_distances()
        distances.sort()
        for i in range(len(distances)):
            for j in range(int(self.data["taxon_number"])):
                pass


