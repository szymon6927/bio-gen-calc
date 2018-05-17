$(document).ready(function () {
  const chiArray = new ChiSquareArray('.array-wrapper');
  $('.generate-array').click( (e) => {
    console.log("click");
    let width = $('.array-width').val();
    let height = $('.array-height').val();

    console.log(width, height);

    chiArray.setWidth(width);
    chiArray.setHeight(height);

    chiArray.draw();
  });

  $('.calcuate-button').click( () => {
    chiArray.calacute();
  });
});