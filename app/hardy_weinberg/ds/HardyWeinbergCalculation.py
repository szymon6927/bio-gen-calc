from typing import Tuple

import numpy as np
from scipy.stats import chisquare
from scipy.stats import power_divergence

from app.common.result_aggregator import add_result
from app.hardy_weinberg.ds.types import Num
from app.hardy_weinberg.ds.types import PowerDivergence
from app.hardy_weinberg.ds.types import Result
from app.hardy_weinberg.entities.hw_entity import HWEntity


class HardyWeinbergCalculation:
    def __init__(self, data: HWEntity) -> None:
        self.data: HWEntity = data
        self.results: Result = []

    def calculate_expected_observed(self) -> Tuple[Num, Num, Num, Num, Num, Num, Num, Num]:
        ho: int = self.data.ho
        he: int = self.data.he
        rho: int = self.data.rho

        sum_val: int = ho + he + rho

        n: float = 2 * (ho + he + rho)

        p: float = ((2 * ho) + he) / n
        q: float = ((2 * rho) + he) / n

        e_ho: float = (p ** 2) * sum_val
        e_he: float = (2 * p * q) * sum_val
        e_rho: float = (q ** 2) * sum_val

        return ho, he, rho, e_ho, e_he, e_rho, p, q

    def calculate_yates_correction(self) -> PowerDivergence:
        ho, he, rho, e_ho, e_he, e_rho, p, q = self.calculate_expected_observed()

        observed: np.ndarray = np.asarray([ho, he, rho])
        expected: np.ndarray = np.asarray([e_ho, e_he, e_rho])
        dof: int = 2

        observed = observed + 0.5 * np.sign(expected - observed)

        return power_divergence(observed, expected, ddof=observed.size - 1 - dof, axis=None, lambda_=None)

    def calculate(self) -> Result:
        alfa: float = self.data.alfa
        ho, he, rho, e_ho, e_he, e_rho, p, q = self.calculate_expected_observed()
        chi, pval = chisquare([ho, he, rho], f_exp=[e_ho, e_he, e_rho])

        add_result(self, 'expected number of homozygotes', round(e_ho, 2))
        add_result(self, 'expected number of heterozygotes', round(e_he, 2))
        add_result(self, 'expected number of rare homozygotes', round(e_rho, 2))
        add_result(self, 'p', round(p, 5))
        add_result(self, 'q', round(q, 5))
        add_result(self, 'p-value', round(pval, 5))
        add_result(self, 'Chi-square value', round(chi, 5))

        if ho < 5 or he < 5 or rho < 5:
            chi_yates, pval_yates = self.calculate_yates_correction()

            add_result(self, 'Yate`s chi-square value', round(chi_yates, 5))
            add_result(self, 'Yate`s p-value', round(pval_yates, 5))

            # set pval to pval_yates for next if statement
            pval = pval_yates

        if pval <= alfa:
            msg = f"Distribution does not consistent with Hardy Weinberg's law at the level of significance: {alfa}"
            add_result(self, 'status', msg)

            fis: float = 1 - (he / e_he)
            add_result(self, 'fis', round(fis, 4))
        elif pval > alfa:
            msg = f"Distribution consistent with Hardy Weinberg's law at the level of significance: {alfa}"
            add_result(self, 'status', msg)

        return self.results
