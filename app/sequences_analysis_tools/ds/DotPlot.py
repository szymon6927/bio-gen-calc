import base64
from io import BytesIO

import pylab
from Bio import Entrez
from Bio import SeqIO
from Bio import pairwise2

from app.common.result_aggregator import add_result


class DotPlot:
    def __init__(self, data):
        self.data = data
        self.results = []

    def remove_newlines(self):
        self.data['seq-content-1'] = self.data['seq-content-1'].replace('\n', '')
        self.data['seq-content-2'] = self.data['seq-content-2'].replace('\n', '')

    def get_coverage(self):
        coverage_list = []

        coverage1 = len(self.data['seq-content-1']) / len(self.data['seq-content-2']) * 100
        coverage2 = len(self.data['seq-content-2']) / len(self.data['seq-content-1']) * 100

        coverage_list.append(coverage1)
        coverage_list.append(coverage2)

        return round(min(coverage_list), 1)

    def get_alignments(self):
        alignments = pairwise2.align.globalms(self.data['seq-content-1'], self.data['seq-content-2'], 2, -1, -0.5, -0.1)

        string_alignment = pairwise2.format_alignment(*alignments[0])

        return string_alignment

    def get_average_identity(self, ident):
        average_length = (len(self.data['seq-content-1']) + len(self.data['seq-content-2'])) / 2
        average_identity = (ident / average_length) * 100

        return round(average_identity, 1)

    def get_frag_identity(self, ident):
        len_list = []

        len_list.append(len(self.data['seq-content-1']))
        len_list.append(len(self.data['seq-content-2']))

        frag_identity = (ident / min(len_list)) * 100

        return round(frag_identity, 1)

    def get_dot_plot_image(self):
        dict_one = {}
        dict_two = {}

        y = []
        x = []

        rec_one = self.data['seq-content-1']
        rec_one_name = self.data['seq-name-1']

        rec_two = self.data['seq-content-2']
        rec_two_name = self.data['seq-name-2']

        window = 8

        for (seq, section_dict) in [(rec_one.upper(), dict_one), (rec_two.upper(), dict_two)]:
            for i in range(len(seq) - window):
                section = seq[i : i + window]
                try:
                    section_dict[section].append(i)
                except KeyError:
                    section_dict[section] = [i]

        matches = set(dict_one).intersection(dict_two)

        for section in matches:
            for i in dict_one[section]:
                for j in dict_two[section]:
                    x.append(i)
                    y.append(j)

        pylab.cla()
        pylab.gray()
        pylab.scatter(x, y)
        pylab.xlim(0, len(rec_one) - window)
        pylab.ylim(0, len(rec_two) - window)
        pylab.xlabel(f'{rec_one_name} (length {len(rec_one)} bp) ...')
        pylab.ylabel(f'{rec_two_name} (length {len(rec_two)} bp) ...')
        pylab.title("Dot plot - Gene-Calc")

        figfile = BytesIO()
        pylab.savefig(figfile, format='png', dpi=120)
        figfile.seek(0)  # rewind to beginning of file
        figdata_png = figfile.getvalue()  # extract string (stream of bytes)
        figdata_png = base64.b64encode(figdata_png)
        decoded = figdata_png.decode("utf-8")
        pylab.clf()

        return decoded

    def raw_sequence(self):
        self.remove_newlines()

        seq_name_1 = self.data['seq-name-1']
        seq_name_2 = self.data['seq-name-2']
        seq_content_1 = self.data['seq-content-1']
        seq_content_2 = self.data['seq-content-2']

        alignment = self.get_alignments()

        add_result(self, f'Sequence {seq_name_1} length', len(seq_content_1))
        add_result(self, f'Sequence {seq_name_2} length', len(seq_content_2))

        ident = alignment.count("|")

        coverage = self.get_coverage()
        average_identity = self.get_average_identity(ident)
        frag_identity = self.get_frag_identity(ident)

        add_result(self, "Coverage [%]", coverage)
        add_result(self, "Average identity [%]", average_identity)
        add_result(self, "Fragmental identity [%]", frag_identity)

        return self.results

    def genebank_seq(self):
        Entrez.email = "contact@gene-calc.pl"

        with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=self.data['seq-name-1']) as handle:
            seq_record = SeqIO.read(handle, "gb")
            seq_name_1 = str(seq_record.id) + " " + str(seq_record.description)[:25]
            self.data['seq-content-1'] = str(seq_record.seq)
            self.data['seq-name-1'] = seq_name_1

        with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=self.data['seq-name-2']) as handle:
            seq_record = SeqIO.read(handle, "gb")
            seq_name_2 = str(seq_record.id) + " " + str(seq_record.description)[:25]
            self.data['seq-content-2'] = str(seq_record.seq)
            self.data['seq-name-2'] = seq_name_2

        alignment = self.get_alignments()

        add_result(self, f'Seq id. {seq_name_1} ... length [bp]', len(self.data['seq-content-1']))
        add_result(self, f'Seq id. {seq_name_2} ... length [bp]', len(self.data['seq-content-2']))

        ident = alignment.count("|")

        coverage = self.get_coverage()
        average_identity = self.get_average_identity(ident)
        frag_identity = self.get_frag_identity(ident)

        add_result(self, "Coverage [%]", coverage)
        add_result(self, "Average identity [%]", average_identity)
        add_result(self, "Fragmental identity [%]", frag_identity)

        return self.results
