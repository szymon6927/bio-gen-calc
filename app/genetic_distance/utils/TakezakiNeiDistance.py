from .GeneticDistance import GeneticDistance
from math import sqrt


class TakezakiNeiDistance(GeneticDistance):
    def __init__(self, data):
        super().__init__(data)

    def calcuate_x_y(self):
        sum_product = {}
        pair_combination = self.get_pair_combination(self.column_range)
        for pair in pair_combination:
            product = [sqrt(a * b) for a, b in zip(self.data["column_" + str(pair[0])], self.data["column_" + str(pair[1])])]

            key = f'{pair[0]}_{pair[1]}'
            sum_product[key] = round(sum(i for i in product), 5)

        return sum_product

    def calcuate_distances(self):
        pair_combination = self.get_pair_combination(self.column_range)
        sum_product = self.calcuate_x_y()

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'
            d = 1 - (1 / int(self.data["locus_number"]) * sum_product[key])
            self.distances.append(round(d, 5))

        self.condensed_matrix = self.distances[:]

