const moduleSections = '.raw-sequences, .sequences-form-genebank';
const moduleResultsSection = '.raw-seq-results, .genebank-seq-results';

const dotPlot = new DotPlot();

$('#type-of-data').change(function () {
  $(moduleSections).hide();
  $(moduleResultsSection).empty();

  let type = $(this).val();
  
  $('.dot-plot select option').removeAttr('selected');
  $(`.dot-plot select option[value='${type}']`).attr("selected","selected");

  $(`.${type}`).show();
});


$('.dot-plot-raw-calculate').click(function () {
  dotPlot.sendRawSeq();
});

$('.dot-plot-genebank-calculate').click(function () {
  dotPlot.sendSeqGeneBank();
});

$('.raw-sequences .form-control').keypress(function (e) {
  if (e.which == 13) {
    $('.dot-plot-raw-calculate').trigger('click');
    return false;
  }
});

$('.sequences-form-genebank .form-control').keypress(function (e) {
  if (e.which == 13) {
    $('.dot-plot-genebank-calculate').trigger('click');
    return false;
  }
});