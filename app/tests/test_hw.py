from ..hardy_weinber.utils.HardyWeinberCalculation import HardyWeinberCalculation


def test_hw_basic():
    data = dict()
    data["ho"] = 4
    data["he"] = 3
    data["rho"] = 2
    data["alfa"] = 0.05

    hw = HardyWeinberCalculation(data)
    results = hw.calcualte()

    expected_results = [3.36, 4.28, 1.36, 0.61111, 0.38889, 0.66931, 0.8,
                        "Distribution consistent with Hardy Weinberg's law at the level of significance: 0.05"]

    for i, result in enumerate(results):
        assert result.get("value") == expected_results[i]


