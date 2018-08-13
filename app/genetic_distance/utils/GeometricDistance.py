from itertools import islice
from .GeneticDistance import GeneticDistance
from scipy.stats.mstats import gmean


class GeometricDistance(GeneticDistance):
    def __init__(self, data):
        super().__init__(data)
        self.column_geo_avg = dict()

    def calculate_square_sum(self):
        g_square_sum = dict()
        g_sizes = self.data['number_of_alleles']
        column_count = int(self.data['taxon_number'])

        for i in range(column_count):
            all_column_values = self.data[f'column_{str(i)}']

            it = iter(all_column_values)
            column_sliced = [list(islice(it, 0, i)) for i in g_sizes]

            square_sum_list = []
            for g_list in column_sliced:
                square_sum = sum(j*j for j in g_list)
                square_sum_list.append(square_sum)

            print(f'{i} - {square_sum_list}', flush=True)
            g_square_sum[i] = square_sum_list

        return g_square_sum

    def calculate_geometric_avg(self):
        g_square_sum = self.calculate_square_sum()

        for key, value_list in g_square_sum:
            square_sum_list = g_square_sum[key]
            self.column_geo_avg[key] = gmean(square_sum_list)

    def calcuate_distances(self):
        print("test", flush=True)
        self.calculate_geometric_avg()
        print("Geomatric distane for columns", flush=True)
