class Codominant:
    def __init__(self, data):
        self.result = {}
        self.data = data

    def get_alleles_sum(self):
        alleles_list = []
        for i in range(self.data["count"]):
            alleles_list.append(int(self.data["allele-" + str(i)]))

        return sum(alleles_list)

    def get_alleles_freq(self):
        p = {}
        alleles_sum = self.get_alleles_sum()

        for i in range(self.data["count"]):
            alleles = int(self.data["allele-" + str(i)])
            p[i] = alleles / alleles_sum

        return p

    def calcuate_h(self):
        freq_sum = 0
        alleles_freq = self.get_alleles_freq()
        for i in range(self.data["count"]):
            freq_sum += alleles_freq[i] ** 2

        result = 1 - freq_sum
        return result

    def calcuate_pic(self):
        sum_pi = 0
        sum_pj = 0

        h = self.calcuate_h()

        alleles_freq = self.get_alleles_freq()
        for i in range(self.data["count"] - 1):
            sum_pi += alleles_freq[i] ** 2

        for i in range(1, self.data["count"] - 1):
            sum_pj += alleles_freq[i] ** 2

        pic = h - (2 * sum_pi * sum_pj)
        return pic

    def calculate(self):
        self.result["H"] = self.calcuate_h()
        self.result["PIC"] = self.calcuate_pic()
        return self.result


class Dominant:
    def __init__(self, data):
        self.result = {}
        self.data = data

    def print_data(self):
        print(self.data, flush=True)

    def calculate(self):
        fi = float(self.data["amplified_marker"]) / (float(self.data["amplified_marker"]) + float(
            self.data["absecnce_marker"]))
        pic = 2 * fi * (1 - fi)
        self.result["PIC"] = pic
        return self.result