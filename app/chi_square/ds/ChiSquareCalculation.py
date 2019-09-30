from math import sqrt

import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import power_divergence
from scipy.stats.contingency import expected_freq

from app.common.result_aggregator import add_result


class ChiSquareCalculation:
    def __init__(self, data):
        self.data = data
        self.results = []

    def get_observed(self):
        all_lists = []
        for i in range(self.data["height"]):
            row = self.data["row-" + str(i)]
            float_row = list(map(float, row))
            all_lists.append(float_row)

        observed = np.array(all_lists)
        return observed

    def chi_square_standard(self):
        return chi2_contingency(self.get_observed(), correction=False)

    def chi_square_yats(self):
        observed_list = [self.get_observed()]
        observed = np.asarray(observed_list)
        expected = expected_freq(observed)
        dof = expected.size - sum(expected.shape) + expected.ndim - 1
        observed = observed + 0.5 * np.sign(expected - observed)

        return power_divergence(observed, expected, ddof=observed.size - 1 - dof, axis=None, lambda_=None)

    def correlation(self):
        field_sum = float(self.data["field_sum"])
        chi2_standard, p_standard, dof, ex = self.chi_square_standard()
        chi2_yats, p_yats = self.chi_square_yats()

        if dof == 1:
            correlation_standard = sqrt(chi2_standard / field_sum)
            correlation_yats = sqrt(chi2_yats / field_sum)
            add_result(self, "coefficient of contingency type", "Phi")
        else:
            m = min(self.data["width"], self.data["height"])
            correlation_standard = sqrt(chi2_standard / (field_sum * (m - 1)))
            correlation_yats = sqrt(chi2_yats / (field_sum * (m - 1)))
            add_result(self, "coefficient of contingency type", "Crammer`s V")

        return chi2_standard, p_standard, dof, chi2_yats, p_yats, correlation_standard, correlation_yats

    def calculate(self):
        chi2_standard, p_standard, dof, chi2_yats, p_yats, correlation_standard, corelation_yats = self.correlation()
        add_result(self, "dof", dof)
        add_result(self, "chi2_standard", round(chi2_standard, 5))
        add_result(self, "p_standard", round(p_standard, 5))
        add_result(self, "correlation_standard", round(correlation_standard, 5))
        add_result(self, "chi2_yats", round(chi2_yats, 5))
        add_result(self, "p_yats", round(p_yats, 5))
        add_result(self, "correlation_yats", round(corelation_yats, 5))

        return self.results
