/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', '/static/js/assets/particles.json', function () {
  console.log('callback - particles.js config loaded');
});

$(document).ready(function () {

  var currentUrl = window.location.href;
  if (currentUrl.includes("herokuapp.com")) {
    window.location.replace("https://gene-calc.pl/");
  }

  $("#back-top").hide();
  $(function () {
    $(window).scroll(function () {
      if ($(this).scrollTop() > 100) {
        $('#back-top').fadeIn();
      } else {
        $('#back-top').fadeOut();
      }
    });
    $('#back-top').click(function () {
      $('body,html').animate({
        scrollTop: 0
      },'slow');
      return false;
    });
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
    footerTop = ($(window).scrollTop() + $(window).height() - footerHeight - 53) + "px";

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