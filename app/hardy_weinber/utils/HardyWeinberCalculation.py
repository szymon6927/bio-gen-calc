from scipy.stats import chisquare


class HardyWeinberCalculation:

    def __init__(self, data):
        self.data = data
        self.results = []

    def add_result(self, name, value):
        self.results.append({'name': name, 'value': value})

    def calcuate_expected_observed(self):
        ho = self.data["ho"]
        he = self.data["he"]
        rho = self.data["rho"]

        sum_val = ho + he + rho

        n = 2 * (ho + he + rho)

        p = ((2 * ho) + he) / n
        q = ((2 * rho) + he) / n

        e_ho = (p ** 2) * sum_val
        e_he = (2 * p * q) * sum_val
        e_rho = (q ** 2) * sum_val

        return ho, he, rho, e_ho, e_he, e_rho, p, q

    def calcualte(self):
        alfa = self.data["alfa"]
        ho, he, rho, e_ho, e_he, e_rho, p, q = self.calcuate_expected_observed()
        chi, pval = chisquare([ho, he, rho], f_exp=[e_ho, e_he, e_rho])

        self.add_result('e_ho', round(e_ho, 2))
        self.add_result('e_he', round(e_he, 2))
        self.add_result('e_rho', round(e_rho, 2))
        self.add_result('p', round(p, 5))
        self.add_result('q', round(q, 5))
        self.add_result('p_value', round(pval, 5))
        self.add_result('chi_square', round(chi, 2))

        if pval <= alfa:
            msg = "Distribution does not consistent with Hardy Weinberg's law at the level " \
                  "of significance: {}".format(alfa)
            self.add_result('status', msg)

            fis = 1 - (he / e_he)
            self.add_result('fis', round(fis, 4))
        elif pval > alfa:
            msg = "Distribution consistent with Hardy Weinberg's law at the level of significance: {}".format(alfa)
            self.add_result('status', msg)

        return self.results
