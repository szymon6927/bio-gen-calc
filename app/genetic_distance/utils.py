import numpy as np


class GeneticDistance:

    def __init__(self, data):
        self.data = data

    def calcuate_estimators(self):
        estimators = {}
        arr = np.array()
        for i in range(0, int(self.data["locus_number"])):
            alleles_nubmer = self.data["g_" + i]["nubmer_of_alleles"]
            for j in range(0, int(alleles_nubmer)):
                arr += self.data["g_" + i]["alleles_" + j]

    def multiply_lists(self, list_a, list_b):
        pass
