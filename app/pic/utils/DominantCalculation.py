from ...helpers.result_aggregator import add_result


class Dominant:
    def __init__(self, data):
        self.data = data
        self.results = []

    def calculate(self):
        # check if type is float change math formula
        if isinstance(self.data["amplified_marker"], float):
            fi = self.data["amplified_marker"]
        else:
            fi = int(self.data["amplified_marker"]) / (int(self.data["amplified_marker"]) + int(
                self.data["absecnce_marker"]))

        pic = 1 - (fi ** 2 + ((1 - fi) ** 2))

        add_result(self, "PIC", round(pic, 4))
        return self.results
