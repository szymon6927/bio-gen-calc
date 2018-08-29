from Bio import AlignIO
from Bio.Align.Applications import MuscleCommandline
from io import StringIO
from Bio.Align import AlignInfo
from ...helpers.result_aggregator import add_result
from ...helpers.file_helper import create_seq_file, remove_temp_file


class ConsensusSequence:
    def __init__(self, data):
        self.data = data
        self.results = []

    def raw_sequence(self):
        filename = create_seq_file(self.data['sequences'])

        muscle = MuscleCommandline(input=filename)
        stdout, stderr = muscle()
        align = AlignIO.read(StringIO(stdout), "fasta")

        summary_align = AlignInfo.SummaryInfo(align)
        consensus = summary_align.gap_consensus(threshold=0.55, ambiguous='N')

        add_result(self, 'Consenus sequecne', str(consensus))
        add_result(self, 'Sequence length', len(consensus))

        remove_temp_file(filename)

        return self.results

    def file_seq(self):
        filename = create_seq_file(self.data['sequences'])

        muscle = MuscleCommandline(input=filename)
        stdout, stderr = muscle()
        align = AlignIO.read(StringIO(stdout), "fasta")

        summary_align = AlignInfo.SummaryInfo(align)
        consensus = summary_align.gap_consensus(threshold=0.55, ambiguous='N')

        remove_temp_file(filename)

        return str(consensus)

