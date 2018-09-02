from flask import abort, Response
import itertools
from ...helpers.result_aggregator import add_result


class Codominant:
    def __init__(self, data):
        self.data = data
        self.results = []

    def get_alleles_sum(self):
        alleles_list = []
        for i in range(self.data["count"]):
            alleles_list.append(int(self.data["allele-" + str(i)]))

        return sum(alleles_list)

    def get_alleles_freq(self):
        control_sum = 0
        p = {}
        alleles_sum = self.get_alleles_sum()

        for i in range(self.data["count"]):
            alleles = self.data["allele-" + str(i)]
            if isinstance(alleles, float):
                p[i] = alleles
            else:
                p[i] = alleles / alleles_sum

            control_sum += p[i]

        if control_sum == 1:
            return p
        else:
            raise ValueError("Mixed type of input values")

    def calcuate_h(self):
        freq_sum = 0
        alleles_freq = self.get_alleles_freq()
        for i in range(self.data["count"]):
            freq_sum += alleles_freq[i] ** 2

        result = 1 - freq_sum
        return round(result, 4)

    def calcuate_pic(self):
        pic = 0
        alleles_freq = self.get_alleles_freq()
        alleles_list = [i for i in range(0, self.data["count"])]
        alleles_pairs = list(itertools.permutations(alleles_list, 2))
        for pair in alleles_pairs:
            geno_type_i = pair[0]
            geno_type_j = pair[1]
            pic += (alleles_freq[geno_type_i] * alleles_freq[geno_type_j]) * (
                        1.0 - (alleles_freq[geno_type_i] * alleles_freq[geno_type_j]))

        return round(pic, 4)

    def calculate(self):
        add_result(self, "H", self.calcuate_h())
        add_result(self, "PIC", self.calcuate_pic())
        return self.results
