const chiArray = new ChiSquareArray('.array-wrapper');
$('.generate-array').click((e) => {
  console.log("click");
  let width = $('.array-width').val();
  let height = $('.array-height').val();

  console.log(width, height);

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