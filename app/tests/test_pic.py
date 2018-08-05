from ..pic.utils.DominantCalculation import Dominant
from ..pic.utils.CodominantCalculation import Codominant


def test_pic_dominant_basic():
    data = dict()
    data["amplified_marker"] = 2
    data["absecnce_marker"] = 3

    pic_dominant = Dominant(data)
    results = pic_dominant.calculate()

    expected_results = [0.48]

    for i, result in enumerate(results):
        assert result.get("value") == expected_results[i]


def test_pic_codominant_basic():
    data = dict()
    data["count"] = 3
    data["allele-0"] = 4
    data["allele-1"] = 2
    data["allele-2"] = 3

    pic_codominant = Codominant(data)
    results = pic_codominant.calculate()

    expected_results = [0.642, 0.5676]

    for i, result in enumerate(results):
        assert result.get("value") == expected_results[i]
