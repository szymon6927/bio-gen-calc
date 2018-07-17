const chiArray = new ChiSquareArray('.array-wrapper');
$('.generate-array').click((e) => {
  let width = $('.array-width').val();
  let height = $('.array-height').val();

  if (!width || !height) {
    showModal('Fill width or height!')
    return false
  }

  chiArray.setWidth(width);
  chiArray.setHeight(height);

  chiArray.draw();

  setTimeout(() => {
    validateNegative()
  },500)
});

$('.calcuate-button').click(() => {
  chiArray.calacute();
  chiArray.sendData();
});