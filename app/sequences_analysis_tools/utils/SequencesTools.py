from flask import abort, Response
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from ...helpers.result_aggregator import add_result


class SequencesTools:
    def __init__(self, data):
        self.data = data
        self.seq_names = []
        self.seq_contents = []
        self.results = []

    def get_seq_names_and_contents(self):
        lines = self.data['sequences'].split('\n')
        raw_seq = ""
        for line in lines:
            if line.startswith('>'):
                self.seq_names.append(line)
                if raw_seq:
                    self.seq_contents.append(raw_seq.rstrip().upper())
                    raw_seq = ""
            else:
                raw_seq += line

        self.seq_contents.append(raw_seq.rstrip().upper())

    def complement_sequences(self):
        self.get_seq_names_and_contents()

        for seq_name, seq in zip(self.seq_names, self.seq_contents):
            raw_seq = Seq(seq, IUPAC.unambiguous_dna)
            transformated_seq = raw_seq.complement()

            add_result(self, seq_name, str(transformated_seq))

    def reverse_and_complement_sequences(self):
        self.get_seq_names_and_contents()

        for seq_name, seq in zip(self.seq_names, self.seq_contents):
            raw_seq = Seq(seq, IUPAC.unambiguous_dna)
            transformated_seq = raw_seq.reverse_complement()

            add_result(self, seq_name, str(transformated_seq))

    def reverse_sequence(self):
        self.get_seq_names_and_contents()

        for seq_name, seq in zip(self.seq_names, self.seq_contents):
            raw_seq = Seq(seq, IUPAC.unambiguous_dna)
            transformated_seq = str(raw_seq[::-1])

            add_result(self, seq_name, transformated_seq)

    def transcribed_sequence(self):
        self.get_seq_names_and_contents()

        for seq_name, seq in zip(self.seq_names, self.seq_contents):
            raw_seq = Seq(seq, IUPAC.unambiguous_dna)
            transformated_seq = raw_seq.transcribe()

            add_result(self, seq_name, str(transformated_seq))

    def translated_sequence(self):
        self.get_seq_names_and_contents()

        for seq_name, seq in zip(self.seq_names, self.seq_contents):
            raw_seq = Seq(seq, IUPAC.unambiguous_dna)
            transcribed = raw_seq.transcribe()
            translated = transcribed.translate()

            add_result(self, seq_name, str(translated))

    def calculate(self):
        transformation_type = self.data['type']
        if transformation_type == 'complement':
            self.complement_sequences()
        elif transformation_type == 'reverse_and_complement':
            self.reverse_and_complement_sequences()
        elif transformation_type == 'reverse':
            self.reverse_sequence()
        elif transformation_type == 'transcription':
            self.transcribed_sequence()
        elif transformation_type == 'translation_to_amino_acid':
            self.translated_sequence()
        else:
            return abort(Response('Please specify transformation type', 400))

        return self.results
