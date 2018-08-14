import itertools
from .GeneticDistance import GeneticDistance
from scipy.stats.mstats import gmean
from math import sqrt, log


class GeometricDistance(GeneticDistance):
    def __init__(self, data):
        super().__init__(data)

    def get_sliced_column(self, column_values):
        """
        :param column_values:
        :return: sliced column values according to number_of_alleles
        """
        g_sizes = self.data['number_of_alleles']
        it = iter(column_values)
        return [list(itertools.islice(it, 0, i)) for i in g_sizes]

    def calculate_square_sum(self):
        g_square_sum = dict()

        for i in range(self.column_range):
            all_column_values = self.data[f'column_{str(i)}']

            column_sliced = self.get_sliced_column(all_column_values)

            square_sum_list = []
            for g_list in column_sliced:
                square_sum = sum(j*j for j in g_list)
                square_sum_list.append(square_sum)

            g_square_sum[i] = square_sum_list

        return g_square_sum

    def calculate_geometric_avg(self):
        """
        :return: dict of gmean from sum of square alleses frequencies for each column
        """
        column_geo_avg = dict()
        g_square_sum = self.calculate_square_sum()

        for key, value_list in g_square_sum.items():
            square_sum_list = g_square_sum[key]
            column_geo_avg[key] = gmean(square_sum_list)

        return column_geo_avg

    def calcuate_products_of_frequency(self):
        """
        :return: dict of gmean of alleles frequencies products between populations for each columns pairs
        """
        dict_of_geomean_Jxy = {}
        pair_combination = self.get_pair_combination(self.column_range)

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'

            column_1 = self.data[f'column_{pair[0]}']
            column_2 = self.data[f'column_{pair[1]}']

            sliced_1 = self.get_sliced_column(column_1)
            sliced_2 = self.get_sliced_column(column_2)

            list_of_jxy = []
            for i in range(int(self.data['locus_number'])):
                jxy = sum([x * y for x, y in zip(sliced_1[i], sliced_2[i])])
                list_of_jxy.append(jxy)

            dict_of_geomean_Jxy[key] = gmean(list_of_jxy)

        return dict_of_geomean_Jxy

    def calcuate_distances(self):
        pair_combination = self.get_pair_combination(self.column_range)
        geo_avg = self.calculate_geometric_avg()
        dict_of_geomean_Jxy = self.calcuate_products_of_frequency()

        for pair in pair_combination:
            key = f'{pair[0]}_{pair[1]}'
            Jx = geo_avg[pair[0]]
            Jy = geo_avg[pair[1]]

            i = dict_of_geomean_Jxy[key] / sqrt(Jx * Jy)
            d = -1 * log(i)

            self.distances.append(round(d, 5))

        self.condensed_matrix = self.distances[:]
