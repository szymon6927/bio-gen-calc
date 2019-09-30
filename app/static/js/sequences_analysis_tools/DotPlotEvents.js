"use strict";

const moduleSections = '.raw-sequences, .sequences-form-genebank';

const dotPlot = new DotPlot();

$('#type-of-data').change(function () {
  $(moduleSections).hide();

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

$('.raw-sequences .save-calculation-form').submit(function(e) {
  e.preventDefault();
  dotPlot.setContainer('.raw-sequences');
  dotPlot.saveCalculation();
});

$('.sequences-form-genebank .save-calculation-form').submit(function(e) {
  e.preventDefault();
  dotPlot.setContainer('.sequences-form-genebank');
  dotPlot.saveCalculation();
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
