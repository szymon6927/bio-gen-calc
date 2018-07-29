from scipy.stats import chisquare


class HardyWeinberCalculation:

    def __init__(self, data):
        self.data = data
        self.result = []

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

        self.result.append({'name': 'e_ho', 'value': round(e_ho, 2)})
        self.result.append({'name': 'e_he', 'value': round(e_he, 2)})
        self.result.append({'name': 'e_rho', 'value': round(e_rho, 2)})
        self.result.append({'name': 'p', 'value': round(p, 5)})
        self.result.append({'name': 'q', 'value': round(q, 5)})
        self.result.append({'name': 'p_value', 'value': round(pval, 5)})
        self.result.append({'name': 'chi_square', 'value': round(chi, 2)})

        if pval <= alfa:
            self.result.append(
                {'name': 'status',
                 'value': "Distribution does not consistent with Hardy Weinberg's law at the level of significance: {}".format(
                     alfa)
                 }
            )

            fis = 1 - (he / e_he)
            fis_round = round(fis, 4)
            self.result.append({'name': 'fis', 'value': fis_round})
        elif pval > alfa:
            self.result.append(
                {'name': 'status',
                 'value': "Distribution consistent with Hardy Weinberg's law at the level of significance: {}".format(
                     alfa)
                 }
            )

        return self.result
