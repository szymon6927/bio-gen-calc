from ...helpers.tests_helper import find_value_by_name
from ...chi_square.utils.ChiSquareGoodness import ChiSquareGoodness


def test_chi_sqaure_goodness_basic():
    data = dict()
    data['observed'] = [4.0, 3.0, 2.0]
    data['expected'] = [3.0, 2.0, 4.0]

    expected_results = [
        {'name': "Chi square", 'value': 1.83333},
        {'name': "Chi square p-value", 'value': 0.39985},
        {'name': "dof", 'value': 2},
        {'name': "Chi square p-value", 'value': 0.72494},
        {'name': "Yate`s Chi square", 'value': 0.77083},
        {'name': "Yate`s Chi square p-value", 'value': 0.68017}
    ]

    chi_square_goodness = ChiSquareGoodness(data['observed'], data['expected'])
    results = chi_square_goodness.calculate()

    for result in results:
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
