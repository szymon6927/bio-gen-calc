import pylab
from io import BytesIO
import base64
from Bio import pairwise2, Entrez, SeqIO
from ...helpers.result_aggregator import add_result


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
        alignments = pairwise2.align.globalxx(self.data['seq-content-1'], self.data['seq-content-2'])

        string_alignment = pairwise2.format_alignment(*alignments[0])

        return string_alignment

    def get_average_identifity(self, ident):
        average_lenght = (len(self.data['seq-content-1']) + len(self.data['seq-content-2'])) / 2
        average_identifity = (ident / average_lenght) * 100

        return round(average_identifity, 1)

    def get_frag_identifity(self, ident):
        len_list = []

        len_list.append(len(self.data['seq-content-1']))
        len_list.append(len(self.data['seq-content-2']))

        frag_identifity = (ident / min(len_list)) * 100

        return round(frag_identifity, 1)

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

        for (seq, section_dict) in [(rec_one.upper(), dict_one),
                                    (rec_two.upper(), dict_two)]:
            for i in range(len(seq) - window):
                section = seq[i:i + window]
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
        pylab.xlabel(f'{rec_one_name[:20]} (length {len(rec_one)} bp) ...')
        pylab.ylabel(f'{rec_two_name[:20]} (length {len(rec_two)} bp) ...')
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

        add_result(self, f'Sequence {seq_name_1} lenght', len(seq_content_1))
        add_result(self, f'Sequence {seq_name_2} lenght', len(seq_content_2))

        ident = alignment.count("|")

        coverage = self.get_coverage()
        average_identifity = self.get_average_identifity(ident)
        frag_identifity = self.get_frag_identifity(ident)

        add_result(self, "Coverage [%]", coverage)
        add_result(self, "Average identity [%]", average_identifity)
        add_result(self, "Fragmental identity [%]", frag_identifity)

        return self.results

    def genebank_seq(self):
        Entrez.email = "contact@gene-calc.pl"

        with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=self.data['seq-name-1']) as handle:
            seq_record = SeqIO.read(handle, "gb")
            self.data['seq-content-1'] = seq_record.seq

        with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=self.data['seq-name-2']) as handle:
            seq_record = SeqIO.read(handle, "gb")
            self.data['seq-content-2'] = seq_record.seq

        seq_name_1 = self.data['seq-name-1']
        seq_name_2 = self.data['seq-name-2']

        alignment = self.get_alignments()

        add_result(self, f'Sequence {seq_name_1} lenght', len(self.data['seq-content-1']))
        add_result(self, f'Sequence {seq_name_2} lenght', len(self.data['seq-content-2']))

        ident = alignment.count("|")

        coverage = self.get_coverage()
        average_identifity = self.get_average_identifity(ident)
        frag_identifity = self.get_frag_identifity(ident)

        add_result(self, "Coverage [%]", coverage)
        add_result(self, "Average identity [%]", average_identifity)
        add_result(self, "Fragmental identity [%]", frag_identifity)

        return self.results
