import numpy as np
from scipy.stats import chisquare
from scipy.stats import power_divergence
from ...helpers.result_aggregator import add_result


class HardyWeinberCalculation:

    def __init__(self, data):
        self.data = data
        self.results = []

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

    def calcualte_yates_correction(self):
        ho, he, rho, e_ho, e_he, e_rho, p, q = self.calcuate_expected_observed()

        observed = np.asarray([ho, he, rho])
        expected = np.asarray([e_ho, e_he, e_rho])
        dof = 2
        observed = observed + 0.5 * np.sign(expected - observed)

        return power_divergence(observed, expected, ddof=observed.size - 1 - dof, axis=None, lambda_=None)

    def calcualte(self):
        alfa = self.data["alfa"]
        ho, he, rho, e_ho, e_he, e_rho, p, q = self.calcuate_expected_observed()
        chi, pval = chisquare([ho, he, rho], f_exp=[e_ho, e_he, e_rho])

        add_result(self, 'expected number of homozygotes', round(e_ho, 2))
        add_result(self, 'expected number of heterozygotes', round(e_he, 2))
        add_result(self, 'expected number of rare homozygotes', round(e_rho, 2))
        add_result(self, 'p', round(p, 5))
        add_result(self, 'q', round(q, 5))
        add_result(self, 'p-value', round(pval, 5))
        add_result(self, 'Chi-square value', round(chi, 5))

        if ho < 5 or he < 5 or rho < 5:
            chi_yates, pval_yates = self.calcualte_yates_correction()

            add_result(self, 'Yate`s chi-square value', round(chi_yates, 5))
            add_result(self, 'Yate`s p-value', round(pval_yates, 5))

            # set pval to pval_yates for next if statement ~JANO
            pval = pval_yates

        if pval <= alfa:
            msg = "Distribution does not consistent with Hardy Weinberg's law at the level " \
                  "of significance: {}".format(alfa)
            add_result(self, 'status', msg)

            fis = 1 - (he / e_he)
            add_result(self, 'fis', round(fis, 4))
        elif pval > alfa:
            msg = "Distribution consistent with Hardy Weinberg's law at the level of significance: {}".format(alfa)
            add_result(self, 'status', msg)

        return self.results
