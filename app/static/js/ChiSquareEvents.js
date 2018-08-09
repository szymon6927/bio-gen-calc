const chiArray = new ChiSquare('.array-wrapper');
const validator = new Validation();

$('.generate-array').click((e) => {
  let width = $('.array-width').val();
  let height = $('.array-height').val();

  if (!width || !height) {
    showModal('Fill width or height!');
    return false
  }

  chiArray.setWidth(width);
  chiArray.setHeight(height);

  chiArray.draw();

  setTimeout(() => {
    validator.nonNegative()
  },500);

  goToByScroll('.array-wrapper');
});

$('.calcuate-button').click(() => {
  chiArray.calacute();
  chiArray.sendData();
  goToByScroll('.chi-result');
});

const chiSquareSection = $('.chi-independence');

$(document).on('keypress', '.array-width, .array-height', function (e) {
  if (e.which == 13) {
    chiSquareSection.find('.generate-array').trigger('click');
    chiSquareSection.find('.cell').first().focus();
    return false;
  }
});

$(document).on('keypress', '.chi-independence .table .form-control', function (e) {
  if (e.which == 13) {
    chiSquareSection.find('.calcuate-button').trigger('click');
    return false;
  }
});