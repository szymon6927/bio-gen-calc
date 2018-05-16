$(document).ready(function () {
  $('.generate-array').click( (e) => {
    console.log("click");
    let width = $('.array-width').val();
    let height = $('.array-height').val();

    console.log(width, height);

    const chiArray = new ChiSquareArray(width, height, '.array-wrapper');
    chiArray.draw();
  });
});