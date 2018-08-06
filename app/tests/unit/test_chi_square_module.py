from ...helpers.tests_helper import find_value_by_name
from ...chi_square.utils.ChiSquareCalculation import ChiSquareCalculation


def test_chi_sqaure_basic():
    data = dict()
    data['row-0'] = [4.0, 4.0]
    data['row-1'] = [2.0, 3.0]
    data['column-0'] = [4.0, 2.0]
    data['column-0'] = [4.0, 3.0]
    data['width'] = 2
    data['height'] = 2
    data['field_sum'] = 13

    expected_results = [
        {'name': "coefficient of contingency type", 'value': "Phi"},
        {'name': "dof", 'value': 1},
        {'name': "Chi square", 'value': 0.12381},
        {'name': "Chi square p-value", 'value': 0.72494},
        {'name': "Chi-square correlation", 'value': 0.09759},
        {'name': "Yate`s Chi square", 'value': 0.04836},
        {'name': "Yate`s Chi square p-value", 'value': 0.82594},
        {'name': "Yate`s chi-square correlation", 'value': 0.06099}
    ]

    chi_square = ChiSquareCalculation(data)
    results = chi_square.calculate()

    for result in results:
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
