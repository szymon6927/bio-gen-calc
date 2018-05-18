from math import sqrt
import numpy as np
from scipy.stats import power_divergence
from scipy.stats.contingency import expected_freq
from scipy.stats import chi2_contingency


class ChiSquareCalculation:
    def __init__(self, data):
        self.data = data
        self.result = {}

    def get_observed(self):
        all_lists = []
        for i in range(self.data["height"]):
            row = self.data["row-" + str(i)]
            int_row = list(map(int, row))
            all_lists.append(int_row)

        observed = np.array(all_lists)
        return observed

    def chi_square_standard(self):
        chi2, p, dof, ex = chi2_contingency(self.get_observed(), correction=False)
        self.result["chi2_standard"] = chi2
        self.result["p_standard"] = p
        self.result["dof"] = dof
        # self.result["expected"] = ex

    def chi_square_yats(self):
        observed_list = [self.get_observed()]
        observed = np.asarray(observed_list)
        expected = expected_freq(observed)
        dof = expected.size - sum(expected.shape) + expected.ndim - 1
        observed = observed + 0.5 * np.sign(expected - observed)
        chi2_yats, p_yats = power_divergence(observed, expected,
                                             ddof=observed.size - 1 - dof, axis=None,
                                             lambda_=None)
        self.result["chi2_yats"] = chi2_yats
        self.result["p_yats"] = p_yats

    def corelation(self):
        field_sum = self.data["width"] + self.data["height"]
        if self.result["dof"] == 1:
            corelation_standard = sqrt(self.result["chi2_standard"] / field_sum)
            corelation_yats = sqrt(self.result["chi2_yats"] / field_sum)
            self.result["yule"] = True
        else:
            m = max(self.data["width"], self.data["height"])
            corelation_standard = sqrt(self.result["chi2_standard"] / field_sum * (m - 1))
            corelation_yats = sqrt(self.result["chi2_yats"] / field_sum * (m - 1))
            self.result["crammer"] = True
        self.result["corelation_standard"] = corelation_standard
        self.result["corelation_yats"] = corelation_yats

    def chi_square(self):
        self.get_observed()
        self.chi_square_standard()
        self.chi_square_yats()
        self.corelation()

        return self.result
