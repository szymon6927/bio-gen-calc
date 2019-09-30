from app.helpers.tests_helper import find_value_by_name
from app.sequences_analysis_tools.ds.DotPlot import DotPlot


def test_dotplot_raw_seq_basic():
    data = dict()
    data['seq-name-1'] = "xxx"
    data['seq-content-1'] = "CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG"
    data['seq-name-2'] = "yyy"
    data['seq-content-2'] = "AATCTGGAGGACCTGTGGTAACTCAGCTCGTCGTGGCACTGCTTTTGTCGTGACCCTGCTTTGTTGTTGG"

    dotplot = DotPlot(data)
    results = dotplot.raw_sequence()

    expected_results = [
        {'name': "Sequence xxx length", 'value': 70},
        {'name': "Sequence yyy length", 'value': 70},
        {'name': "Coverage [%]", 'value': 100},
        {'name': "Average identity [%]", 'value': 61.4},
        {'name': "Fragmental identity [%]", 'value': 61.4},
    ]

    base64_img = dotplot.get_dot_plot_image()
    alignment = dotplot.get_alignments()

    assert isinstance(base64_img, str)
    assert isinstance(alignment, str)

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value


def test_dotplot_genebank_basic():
    data = dict()
    data['seq-name-1'] = "2765658"
    data['seq-name-2'] = "2765657"

    dotplot = DotPlot(data)
    results = dotplot.genebank_seq()

    expected_results = [
        {'name': "Seq id. Z78533.1 C.irapeanum 5.8S rRNA gen ... length [bp]", 'value': 740},
        {'name': "Seq id. Z78532.1 C.californicum 5.8S rRNA  ... length [bp]", 'value': 753},
        {'name': "Coverage [%]", 'value': 98.3},
        {'name': "Average identity [%]", 'value': 82.4},
        {'name': "Fragmental identity [%]", 'value': 83.1},
    ]

    base64_img = dotplot.get_dot_plot_image()
    alignment = dotplot.get_alignments()

    assert isinstance(base64_img, str)
    assert isinstance(alignment, str)

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
