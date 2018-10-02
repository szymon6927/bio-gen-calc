const moduleSections = '.raw-sequences, .upload-sequences, .sequences-form-genebank';
const moduleResultsSection = '.raw-seq-results, .file-seq-results, .file-seq-genebank-results';

const consensusSeq = new ConsensusSequence();

$('#type-of-data').change(function () {
  $(moduleSections).hide();
  $(moduleResultsSection).empty();

  let type = $(this).val();
  
  $('.consensus-sequence select option').removeAttr('selected');
  $(`.consensus-sequence select option[value='${type}']`).attr("selected","selected");

  $(`.${type}`).show();
});

$('.consensus-sequence-calculate.raw-seq').click(function () {
  consensusSeq.sendRawSeq()
});

$('.consensus-sequence-calculate.file-seq').click(function () {
  consensusSeq.sendSeqFile()
});

$('.consensus-sequence-calculate.genebank-seq').click(function () {
  consensusSeq.sendSeqGeneBank()
});