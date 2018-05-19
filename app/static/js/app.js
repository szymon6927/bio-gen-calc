$(document).ready(function () {
  const chiArray = new ChiSquareArray('.array-wrapper');
  $('.generate-array').click((e) => {
    console.log("click");
    let width = $('.array-width').val();
    let height = $('.array-height').val();

    console.log(width, height);

    chiArray.setWidth(width);
    chiArray.setHeight(height);

    chiArray.draw();
  });

  $('.calcuate-button').click(() => {
    chiArray.calacute();
    chiArray.sendData();
  });

  const chiArrayGoodness = new ChiSquareOfGoodness('.array-wrapper-goodness');
  $('.generate-array-goodness').click(() => {
    let width = $('.goodness-width').val();
    chiArrayGoodness.setWidth(width);
    chiArrayGoodness.draw();
  });

  $('.calcuate-button-goodness').click(() => {
    chiArrayGoodness.sendData();
  });
});

$(window).bind("load", function () {

  let footerHeight = 0,
    footerTop = 0,
    $footer = $(".footer");

  positionFooter();

  function positionFooter() {
    footerHeight = $footer.height();
    // 20 is as padding height
    footerTop = ($(window).scrollTop() + $(window).height() - footerHeight - 52) + "px";

    if (($(document.body).height() + footerHeight) < $(window).height()) {
      $footer.css({
        position: "absolute",
        width: "100%"
      }).animate({
        top: footerTop
      })
    }
    else {
      $footer.css({
        position: "static"
      })
    }

  }

  $(window)
    .scroll(positionFooter)
    .resize(positionFooter)
});