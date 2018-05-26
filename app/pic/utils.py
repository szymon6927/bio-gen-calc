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
        return round(result, 4)

    def calcuate_pic(self):
        pic = 0
        alleles_freq = self.get_alleles_freq()
        for i in range(0, self.data["count"]):
            for j in range(0, self.data["count"]):
                if i != j:
                    pic += (alleles_freq[i] * alleles_freq[j]) * (1.0 - (alleles_freq[i] * alleles_freq[j]))

        return round(pic, 4)

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
        fi = int(self.data["amplified_marker"]) / (int(self.data["amplified_marker"]) + int(
            self.data["absecnce_marker"]))
        pic = 1 - (fi ** 2 + ((1 - fi) ** 2))
        self.result["PIC"] = round(pic, 4)
        return self.result
