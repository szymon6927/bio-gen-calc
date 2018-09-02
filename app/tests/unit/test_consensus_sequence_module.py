from ...helpers.tests_helper import find_value_by_name
from ...sequences_analysis_tools.utils.ConsensusSequence import ConsensusSequence


def test_consensus_sequence_raw_seq_basic():
    data = dict()
    data['sequences'] = """>gi|2765658
CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"""

    con_seq = ConsensusSequence(data)
    results = con_seq.raw_sequence()

    expected_results = [
        {'name': "Consenus sequence",
         'value': "CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTGAATCCGGAGGACCGGTGTACTCAGCTCA"
                  "CCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"},
        {'name': "Sequence length", 'value': 140}
    ]

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
