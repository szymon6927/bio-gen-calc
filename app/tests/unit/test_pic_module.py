from ...helpers.tests_helper import find_value_by_name
from ...pic.utils.DominantCalculation import Dominant
from ...pic.utils.CodominantCalculation import Codominant


def test_pic_dominant_basic():
    data = dict()
    data["amplified_marker"] = 2
    data["absecnce_marker"] = 3

    pic_dominant = Dominant(data)
    results = pic_dominant.calculate()

    expected_results = [
        {'name': "PIC", 'value': 0.48}
    ]

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')
        
        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value


def test_pic_codominant_basic():
    data = dict()
    data["count"] = 3
    data["allele-0"] = 4
    data["allele-1"] = 2
    data["allele-2"] = 3

    pic_codominant = Codominant(data)
    results = pic_codominant.calculate()

    expected_results = [
        {'name': "H", 'value': 0.642},
        {'name': "PIC", 'value': 0.5676},
    ]

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')
        
        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
