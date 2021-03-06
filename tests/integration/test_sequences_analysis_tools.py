import json
from io import BytesIO
from unittest.mock import patch

from app.common.constants import ModuleName
from app.userpanel.models import Calculation
from tests.integration.constants import URL


def test_get_dot_plot_ok(test_client):
    response = test_client.get(URL.DOT_PLOT_GET)

    assert response.status_code == 200
    assert b'Dot plot' in response.data


def test_post_dot_plot_raw_seq_ok(test_client):
    data = dict()
    data['seq-name-1'] = "Seq 1"
    data['seq-content-1'] = "CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG"
    data['seq-name-2'] = "Seq 2"
    data['seq-content-2'] = "AATCTGGAGGACCTGTGGTAACTCAGCTCGTCGTGGCACTGCTTTTGTCGTGACCCTGCTTTGTTGTTGG"

    response = test_client.post(URL.DOT_PLOT_RAW_SEQ_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()
    result = json.loads(response.data)

    assert response.status_code == 200
    assert ModuleName.DOT_PLOT_RAW_SEQ in calculation.module_name
    assert 'dotplot_base64' in result
    assert 'alignment' in result


def test_post_dot_plot_gene_bank_ids(test_client):
    data = dict()
    data['seq-name-1'] = "2765658"
    data['seq-name-2'] = "2765657"

    response = test_client.post(URL.DOT_PLOT_GENE_BANK_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()
    result = json.loads(response.data)

    assert response.status_code == 200
    assert ModuleName.DOT_PLOT_GENEBANK_IDS in calculation.module_name
    assert 'dotplot_base64' in result
    assert 'alignment' in result


def test_get_consensus_sequence_ok(test_client):
    response = test_client.get(URL.CONSENSUS_SEQUENCE_GET)

    assert response.status_code == 200
    assert b'Consensus Sequence' in response.data


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_post_consensus_sequence_raw_seq_ok(muscle_command_line_mock, test_client, muscle_standard_seq_return_value):
    muscle_command_line_mock.return_value.return_value = muscle_standard_seq_return_value

    data = dict()
    data[
        'sequences'
    ] = """>gi|2765658
        CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
        AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"""

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_RAW_SEQ_POST, data=json.dumps(data), content_type='application/json'
    )
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.CONSENSUS_SEQUENCE_RAW_SEQ in calculation.module_name


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_post_consensus_sequence_raw_seq_with_threshold_ok(
    muscle_command_line_mock, test_client, muscle_standard_seq_return_value
):
    muscle_command_line_mock.return_value.return_value = muscle_standard_seq_return_value

    data = dict()
    data[
        'sequences'
    ] = """>gi|2765658
            CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
            AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"""
    data['threshold'] = 0.60

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_RAW_SEQ_POST, data=json.dumps(data), content_type='application/json'
    )
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.CONSENSUS_SEQUENCE_RAW_SEQ in calculation.module_name


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_post_consensus_sequence_file_seq_ok(muscle_command_line_mock, test_client, muscle_standard_seq_return_value):
    muscle_command_line_mock.return_value.return_value = muscle_standard_seq_return_value

    data = dict()
    file_content = """>gi|2765658
        CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
        AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG"""
    data['file'] = (BytesIO(file_content.encode()), 'seq.fasta')
    data['threshold'] = 0.55

    response = test_client.post(URL.CONSENSUS_SEQUENCE_FILE_SEQ_POST, data=data, content_type='multipart/form-data')

    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert response.headers.get('content-type') == 'text/plain; charset=utf-8'
    assert ModuleName.CONSENSUS_SEQUENCE_FILE_SEQ in calculation.module_name


def test_post_consensus_sequence_file_seq_no_file(test_client):
    data = dict()
    data['threshold'] = 0.55

    response = test_client.post(URL.CONSENSUS_SEQUENCE_FILE_SEQ_POST, data=data, content_type='multipart/form-data')

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert b'No file part' in response.data
    assert len(calculations) == 0


def test_post_consensus_sequence_file_seq_file_without_name(test_client):
    data = dict()
    data['file'] = (BytesIO(b'Test file seq'), '')
    data['threshold'] = 0.55

    response = test_client.post(URL.CONSENSUS_SEQUENCE_FILE_SEQ_POST, data=data, content_type='multipart/form-data')

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert b'No selected file' in response.data
    assert len(calculations) == 0


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_post_consensus_sequence_gene_bank_seq_protein_ok(
    muscle_command_line_mock, test_client, muscle_gene_bank_protein_return_value
):
    muscle_command_line_mock.return_value.return_value = muscle_gene_bank_protein_return_value

    data = dict()
    data['sequence-type'] = "protein"
    data['genebank-seq'] = "ADZ48385.1\nABM89502.1"

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_GENE_BANK_POST, data=json.dumps(data), content_type='application/json'
    )

    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert response.headers.get('content-type') == 'text/plain; charset=utf-8'
    assert ModuleName.CONSENSUS_SEQUENCE_GENE_BANK in calculation.module_name


def test_post_consensus_sequence_gene_bank_seq_protein_wrong_gene_bank_ids(test_client):
    data = dict()
    data['sequence-type'] = "protein"
    data['genebank-seq'] = "2765658\n2765657"

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_GENE_BANK_POST, data=json.dumps(data), content_type='application/json'
    )

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0


@patch('app.sequences_analysis_tools.ds.ConsensusSequence.MuscleCommandline')
def test_post_consensus_sequence_gene_bank_seq_nucleotide_ok(
    muscle_command_line_mock, test_client, muscle_gene_bank_nucleotide_return_value
):
    muscle_command_line_mock.return_value.return_value = muscle_gene_bank_nucleotide_return_value

    data = dict()
    data['sequence-type'] = "nucleotide"
    data['genebank-seq'] = "2765658\n2765657"

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_GENE_BANK_POST, data=json.dumps(data), content_type='application/json'
    )

    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert response.headers.get('content-type') == 'text/plain; charset=utf-8'
    assert ModuleName.CONSENSUS_SEQUENCE_GENE_BANK in calculation.module_name


def test_post_consensus_sequence_gene_bank_seq_nucleotide_wrong_gene_bank_ids(test_client):
    data = dict()
    data['sequence-type'] = "nucleotide"
    data['genebank-seq'] = "ADZ48385.1\nABM89502.1"

    response = test_client.post(
        URL.CONSENSUS_SEQUENCE_GENE_BANK_POST, data=json.dumps(data), content_type='application/json'
    )

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0


def test_get_sequences_tools_ok(test_client):
    response = test_client.get(URL.SEQUENCES_TOOLS_GET)

    assert response.status_code == 200
    assert b'Sequences Tools' in response.data


def test_post_sequences_tools_ok(test_client):
    data = dict()
    data[
        'sequences'
    ] = """>2765658
CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG
CCGCCTCGGGAGCGTCCATGGCGGGTTTGAACCTCTAGCCCGGCGCAGTTTGGGCGCCAAGCCATATGAA
AGCATCACCGGCGAATGGCATTGTCTTCCCCAAAACCCGGAGCGGCGGCGTGCTGTCGCGTGCCCAATGA


>2765657
CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGTTGAGACAACAGAATATATGATCGAGTG
AATCTGGAGGACCTGTGGTAACTCAGCTCGTCGTGGCACTGCTTTTGTCGTGACCCTGCTTTGTTGTTGG
GCCTCCTCAAGAGCTTTCATGGCAGGTTTGAACTTTAGTACGGTGCAGTTTGCGCCAAGTCATATAAAGC


>2765656
CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGTTGAGACAGCAGAACATACGATCGAGTG
AATCCGGAGGACCCGTGGTTACACGGCTCACCGTGGCTTTGCTCTCGTGGTGAACCCGGTTTGCGACCGG
GCCGCCTCGGGAACTTTCATGGCGGGTTTGAACGTCTAGCGCGGCGCAGTTTGCGCCAAGTCATATGGAG"""

    sequences_types = ['complement', 'reverse_and_complement', 'reverse', 'transcription', 'translation_to_amino_acid']

    for sequence_type in sequences_types:
        data['type'] = sequence_type

        response = test_client.post(URL.SEQUENCES_TOOLS_POST, data=json.dumps(data), content_type='application/json')

        calculation = Calculation.query.first()

        assert response.status_code == 200
        assert ModuleName.SEQUENCES_TOOLS in calculation.module_name
