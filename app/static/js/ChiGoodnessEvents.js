const chiArrayGoodness = new ChiSquareOfGoodness('.array-wrapper-goodness');
$('.generate-array-goodness').click(() => {
  let width = $('.goodness-width').val();

  if(!width) {
    showModal('Fill width input!')
    return false
  }

  chiArrayGoodness.setWidth(width);
  chiArrayGoodness.draw();

  setTimeout(() => {
    validateNegative()
  },500)
});

$('.calcuate-button-goodness').click(() => {
  chiArrayGoodness.sendData();
});