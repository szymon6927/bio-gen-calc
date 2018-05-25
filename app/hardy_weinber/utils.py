class HardyWeinberCalculation:
    cirticial_value_1 = 5.9915  # 0.05
    cirticial_value_2 = 9.2104  # 0.01

    def __init__(self, ho, he, rho, critical_select):
        self.ho = ho
        self.he = he
        self.rho = rho
        self.critical_select = critical_select
        self.result = {}

    def __set_given_values(self):
        self.result["given_ho"] = self.ho
        self.result["given_he"] = self.he
        self.result["given_rho"] = self.rho

    def __calcuate_expected(self):
        sum_val = self.ho + self.he + self.rho

        n = 2 * (self.ho + self.he + self.rho)

        p = ((2 * self.ho) + self.he) / n
        q = ((2 * self.rho) + self.he) / n

        expected_ho = (p ** 2) * sum_val
        expected_he = (2 * p * q) * sum_val
        expected_rho = (q ** 2) * sum_val

        self.result["expected_ho"] = expected_ho
        self.result["expected_he"] = round(expected_he, 5)
        self.result["expected_rho"] = round(expected_rho, 5)

    def __calcuate_p_q_n(self):
        n = 2 * (self.ho + self.he + self.rho)

        p = ((2 * self.ho) + self.he) / n
        q = ((2 * self.rho) + self.he) / n

        self.result["n"] = round(n, 5)
        self.result["p"] = round(p, 5)
        self.result["q"] = round(q, 5)

    def __calcaute_chi(self):
        self.__calcuate_expected()
        self.__calcuate_p_q_n()

        if self.ho == 0 or self.he == 0 or self.rho == 0:
            self.result["yats"] = True

            yats_chi_e_ho = ((abs(self.ho - self.result["expected_ho"]) - 0.5) ** 2) / self.result["expected_ho"]
            yats_chi_e_he = ((abs(self.he - self.result["expected_he"]) - 0.5) ** 2) / self.result["expected_he"]
            yats_chi_rho = ((abs(self.rho - self.result["expected_rho"]) - 0.5) ** 2) / self.result["expected_rho"]

            yats_sum_chi = yats_chi_e_ho + yats_chi_e_he + yats_chi_rho
            self.result["yats_sum_chi"] = round(yats_sum_chi, 5)
        else:
            self.result["yats"] = False

        chi_e_ho = ((self.ho - self.result["expected_ho"]) ** 2) / self.result["expected_ho"]
        chi_e_he = ((self.he - self.result["expected_he"]) ** 2) / self.result["expected_he"]
        chi_rho = ((self.rho - self.result["expected_rho"]) ** 2) / self.result["expected_rho"]

        sum_chi = chi_e_ho + chi_e_he + chi_rho
        self.result["sum_chi"] = round(sum_chi, 5)

    def __expolre_critical_values(self):
        self.__calcaute_chi()

        fis = 1 - (self.he / self.result["expected_he"])

        if self.critical_select == "1":
            if self.result["sum_chi"] < self.cirticial_value_1 or (
                    self.result["yats"] is True and self.result["yats_sum_chi"] < self.cirticial_value_1):
                self.result["chi_message"] = "Distribution consistent with Hardy Weinberg's law at the level of significance 0.05"
            else:
                self.result["chi_message"] = "Distribution does not consistent with Hardy Weinberg's law at the level of significance 0.05"
                self.result["fis"] = round(fis, 5)

        if self.critical_select == "2":
            if self.result["sum_chi"] < self.cirticial_value_2 or (
                    self.result["yats"] is True and self.result["yats_sum_chi"] < self.cirticial_value_2):
                self.result["chi_message"] = "Distribution consistent with Hardy Weinberg's law at the level of significance 0.01"
            else:
                self.result["chi_message"] = "Distribution does not consistent with Hardy Weinberg's law at the level of significance 0.01"
                self.result["fis"] = round(fis, 5)

    def get_calculations(self):
        self.__set_given_values()
        self.__expolre_critical_values()
        return self.result
