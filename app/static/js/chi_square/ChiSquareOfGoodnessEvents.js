"use strict";

// validator declared in ChiEvents.js
const chiArrayGoodness = new ChiSquareOfGoodness('.array-wrapper-goodness');
$('.generate-array-goodness').click(() => {
  let width = $('.goodness-width').val();

  if(!width) {
    showModal('Fill width input!');
    return false
  }

  chiArrayGoodness.setWidth(width);
  chiArrayGoodness.draw();

  setTimeout(() => {
    validator.nonNegative()
  },500);

  goToByScroll('.array-wrapper-goodness');
});

$('.calculate-button-goodness').click(() => {
  chiArrayGoodness.sendData();
  goToByScroll('.chi-goodness-result');
});

$('.chi-goodness .save-calculation-form').submit(function(e) {
  e.preventDefault();
  chiArrayGoodness.setContainer('.chi-goodness');
  chiArrayGoodness.saveCalculation();
});

const chiSquareGoodnessSection = $('.chi-goodness');

$(document).on('keypress', '.goodness-width', function (e) {
  if (e.which == 13) {
    chiSquareGoodnessSection.find('.generate-array-goodness').trigger('click');
    chiSquareGoodnessSection.find('.cell').first().focus();
    return false;
  }
});

$(document).on('keypress', '.chi-goodness .table .form-control', function (e) {
  if (e.which == 13) {
    chiSquareGoodnessSection.find('.calculate-button-goodness').trigger('click');
    return false;
  }
});
