const chiArrayGoodness = new ChiSquareOfGoodness('.array-wrapper-goodness');
$('.generate-array-goodness').click(() => {
  let width = $('.goodness-width').val();
  chiArrayGoodness.setWidth(width);
  chiArrayGoodness.draw();
});

$('.calcuate-button-goodness').click(() => {
  chiArrayGoodness.sendData();
});