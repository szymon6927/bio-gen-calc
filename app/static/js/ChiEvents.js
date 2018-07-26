const chiArray = new ChiSquareArray('.array-wrapper');
const validator = new Validation();
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
    validator.nonNegative()
  },500)
});

$('.calcuate-button').click(() => {
  chiArray.calacute();
  chiArray.sendData();
});