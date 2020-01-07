from unittest.mock import patch

from app.helpers.tests_helper import find_value_by_name
from app.sequences_analysis_tools.ds.ConsensusSequence import ConsensusSequence


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_consensus_sequence_raw_seq_basic(muscle_command_line_mock, muscle_standard_seq_return_value):
    muscle_command_line_mock.return_value.return_value = muscle_standard_seq_return_value

    data = dict()
    data[
        'sequences'
    ] = """>gi|2765658
CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"""

    expected_results = [
        {
            'name': "Consensus sequence",
            'value': "CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTGAATCCGGAGGACCGGTGT"
            "ACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG",
        },
        {'name': "Sequence length", 'value': 140},
    ]

    con_seq = ConsensusSequence(data)
    results = con_seq.raw_sequence()

    for i, result in enumerate(results):
        name = result.get('name')
        value = result.get('value')

        expected_value = find_value_by_name(expected_results, name)

        assert expected_value == value
