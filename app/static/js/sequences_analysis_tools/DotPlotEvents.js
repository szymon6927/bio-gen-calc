const moduleSections = '.raw-sequences, .sequences-form-genebank';
const moduleResultsSection = '.raw-seq-results, .genebank-seq-results';

const dotPlot = new DotPlot();

$('#type-of-data').change(function () {
  $(moduleSections).hide();
  $(moduleResultsSection).empty();

  let type = $(this).val();
  $(`.${type}`).show();
});


$('.dot-plot-raw-calculate').click(function () {
  dotPlot.sendRawSeq();
  goToByScroll('.raw-seq-results')
});

$('.dot-plot-genebank-calculate').click(function () {
  dotPlot.sendSeqGeneBank();
});