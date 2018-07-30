import numpy as np
from scipy.stats import power_divergence
from scipy.stats import chisquare
from ...helpers.result_aggregator import add_result


class ChiSquareGoodness:
    def __init__(self, observed, expected):
        self.observed = list(map(float, observed))
        self.expected = list(map(float, expected))
        self.results = []

    def chi_goodness_standard(self):
        chi2, p = chisquare(self.observed, f_exp=self.expected)
        add_result(self, "chi2_standard", round(chi2, 5))
        add_result(self, "p_standard", round(p, 5))
        add_result(self, "dof", len(self.observed) - 1)

    def chi_goodness_yats(self):
        observed = np.asarray(self.observed)
        expected = np.asarray(self.expected)
        observed = observed + 0.5 * np.sign(expected - observed)
        chi2_yats, p_yats = power_divergence(observed, expected, ddof=0)
        add_result(self, "chi2_yats", round(chi2_yats, 5))
        add_result(self, "p_yats", round(p_yats, 5))

    def calculate(self):
        self.chi_goodness_standard()
        self.chi_goodness_yats()
        return self.results

