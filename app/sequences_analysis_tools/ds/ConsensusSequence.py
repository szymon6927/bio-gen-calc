from io import StringIO
from os import environ

from Bio import AlignIO
from Bio import Entrez
from Bio import SeqIO
from Bio.Align import AlignInfo
from Bio.Align.Applications import MuscleCommandline

from app.common.result_aggregator import add_result
from app.helpers.file_helper import create_seq_file
from app.helpers.file_helper import remove_temp_file


class ConsensusSequence:
    def __init__(self, data):
        self.data = data
        self.results = []

    def raw_sequence(self):
        filename = create_seq_file(self.data['sequences'])
        threshold = self.data.get('threshold', 0.55)

        muscle = MuscleCommandline(input=filename)
        stdout, stderr = muscle()
        align = AlignIO.read(StringIO(stdout), "fasta")

        summary_align = AlignInfo.SummaryInfo(align)
        consensus = summary_align.gap_consensus(threshold=threshold, ambiguous='N')

        add_result(self, "Consensus sequence", str(consensus))
        add_result(self, "Sequence length", len(consensus))

        remove_temp_file(filename)

        return self.results

    def file_seq(self):
        filename = create_seq_file(self.data['sequences'])

        threshold = float(self.data.get('threshold'))

        muscle = MuscleCommandline(input=filename)
        stdout, stderr = muscle()
        align = AlignIO.read(StringIO(stdout), "fasta")

        summary_align = AlignInfo.SummaryInfo(align)
        consensus = summary_align.gap_consensus(threshold=threshold, ambiguous='N')

        remove_temp_file(filename)

        return f'>consensus sequence {len(consensus)} bp\n' + str(consensus)

    def genebank_seq(self):
        Entrez.email = environ.get('EMAIL', "contact@gene-calc.pl")

        type_of_seq = self.data['sequence-type']
        lines = self.data['genebank-seq'].split('\n')
        seq_id_list = [line for line in lines if line != '']
        seq_content_list = []

        for seq in seq_id_list:
            with Entrez.efetch(db=type_of_seq, rettype="gb", retmode="text", id=seq) as handle:
                seq_record = SeqIO.read(handle, "gb")
                seq = str(seq_record.seq)
                seq_content_list.append(seq)

        file_content = ""
        for seq_name, seq_content in zip(seq_id_list, seq_content_list):
            file_content += ">" + seq_name + "\n" + seq_content + "\n"

        filename = create_seq_file(file_content)
        threshold = self.data.get('threshold', 0.55)

        muscle = MuscleCommandline(input=filename)
        stdout, stderr = muscle()
        align = AlignIO.read(StringIO(stdout), "fasta")

        summary_align = AlignInfo.SummaryInfo(align)
        consensus = summary_align.gap_consensus(threshold=threshold, ambiguous='N')

        remove_temp_file(filename)

        return f'>consensus sequence {len(consensus)} bp\n' + str(consensus)
