from ...helpers.tests_helper import find_value_by_name
from ...hardy_weinber.utils.HardyWeinberCalculation import HardyWeinberCalculation


def test_hw_basic():
    data = dict()
    data["ho"] = 4
    data["he"] = 3
    data["rho"] = 2
    data["alfa"] = 0.05

    hw = HardyWeinberCalculation(data)
    results = hw.calcualte()

    expected_results = [
        {'name': "expected number of homozygotes", 'value': 3.36},
        {'name': "expected number of heterozygotes", 'value': 4.28},
        {'name': "expected number of rare homozygotes", 'value': 1.36},
        {'name': "p", 'value': 0.61111},
        {'name': "q", 'value': 0.38889},
        {'name': "p-value", 'value': 0.66931},
        {'name': "Chi-square value", 'value': 0.803},
        {'name': "Yate`s chi-square value", 'value': 0.16133},
        {'name': "Yate`s p-value", 'value': 0.9225},
        {'name': "status", 'value': "Distribution consistent with Hardy Weinberg's law at the level of significance: 0.05"}
    ]

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')
        
        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value


