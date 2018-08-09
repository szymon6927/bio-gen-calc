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

$('.calcuate-button-goodness').click(() => {
  chiArrayGoodness.sendData();
  goToByScroll('.chi-goodness-result');
});

const chiSquareGoodenssSection = $('.chi-goodness');

$(document).on('keypress', '.goodness-width', function (e) {
  if (e.which == 13) {
    chiSquareGoodenssSection.find('.generate-array-goodness').trigger('click');
    chiSquareGoodenssSection.find('.cell').first().focus();
    return false;
  }
});

$(document).on('keypress', '.chi-goodness .table .form-control', function (e) {
  if (e.which == 13) {
    chiSquareGoodenssSection.find('.calcuate-button-goodness').trigger('click');
    return false;
  }
});