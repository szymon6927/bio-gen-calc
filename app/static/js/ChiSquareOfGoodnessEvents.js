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