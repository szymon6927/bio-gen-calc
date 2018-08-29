const moduleSections = '.raw-sequences, .upload-sequences, .sequences-form-genebank';
const moduleResultsSection = '.raw-seq-results, .file-seq-results';

const consensusSeq = new ConsensusSequence()

$('#type-of-data').change(function () {
  $(moduleSections).hide();
  $(moduleResultsSection).empty();

  let type = $(this).val();
  $(`.${type}`).show();
});

$('.consensus-sequence-calculate.raw-seq').click(function () {
  consensusSeq.sendRawSeq()
});

$('.consensus-sequence-calculate.file-seq').click(function (e) {
  consensusSeq.sendSeqFile()
});