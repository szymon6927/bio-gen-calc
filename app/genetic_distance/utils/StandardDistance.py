from .GeneticDistance import GeneticDistance
from math import sqrt, log


class StandardDistance(GeneticDistance):
    def __init__(self, data):
        super().__init__(data)

    def estimate_j(self):
        sum_of_square = {}
        for i in range(self.column_range):
            sum_all = sum(j * j for j in self.data["column_" + str(i)]) / int(self.data["locus_number"])
            sum_of_square["j_" + str(i)] = round(sum_all, 5)

        return sum_of_square

    def calcuate_x_y(self):
        sum_product = {}
        pair_combination = self.get_pair_combination(self.column_range)
        for pair in pair_combination:
            product = [a * b for a, b in zip(self.data["column_" + str(pair[0])], self.data["column_" + str(pair[1])])]

            key = f'{pair[0]}_{pair[1]}'
            sum_product[key] = round(sum(i for i in product) / int(self.data["locus_number"]), 5)

        return sum_product

    def calcuate_distances(self):
        pair_combination = self.get_pair_combination(self.column_range)

        sum_of_square = self.estimate_j()
        sum_product = self.calcuate_x_y()

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'
            sum_one = sum_of_square[f'j_{pair[0]}']
            sum_two = sum_of_square[f'j_{pair[1]}']
            i = sum_product[key] / sqrt(sum_one * sum_two)
            i_log = -1 * log(i)
            self.distances.append(round(i_log, 5))

        self.condensed_matrix = self.distances[:]
