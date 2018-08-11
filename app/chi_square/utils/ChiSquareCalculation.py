from math import sqrt
import numpy as np
from scipy.stats import power_divergence
from scipy.stats.contingency import expected_freq
from scipy.stats import chi2_contingency
from ...helpers.result_aggregator import add_result


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

    def corelation(self):
        field_sum = float(self.data["field_sum"])
        chi2_standard, p_standard, dof, ex = self.chi_square_standard()
        chi2_yats, p_yats = self.chi_square_yats()

        if dof == 1:
            corelation_standard = sqrt(chi2_standard / field_sum)
            corelation_yats = sqrt(chi2_yats / field_sum)
            add_result(self, "coefficient of contingency type", "Phi")
        else:
            m = min(self.data["width"], self.data["height"])
            corelation_standard = sqrt(chi2_standard / (field_sum * (m - 1)))
            corelation_yats = sqrt(chi2_yats / (field_sum * (m - 1)))
            add_result(self, "coefficient of contingency type", "Crammer`s V")

        return chi2_standard, p_standard, dof, chi2_yats, p_yats, corelation_standard, corelation_yats

    def calculate(self):
        chi2_standard, p_standard, dof, chi2_yats, p_yats, corelation_standard, corelation_yats = self.corelation()
        add_result(self, "dof", dof)
        add_result(self, "chi2_standard", round(chi2_standard, 5))
        add_result(self, "p_standard", round(p_standard, 5))
        add_result(self, "corelation_standard", round(corelation_standard, 5))
        add_result(self, "chi2_yats", round(chi2_yats, 5))
        add_result(self, "p_yats", round(p_yats, 5))
        add_result(self, "corelation_yats", round(corelation_yats, 5))

        return self.results


