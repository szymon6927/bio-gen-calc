/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', '/static/js/assets/particles.json', function () {
  console.log('callback - particles.js config loaded');
});

$(document).ready(function () {
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
      }, 1500);
      return false;
    });
  });
});

$(window).bind("load", function () {
  positionFooter();
});

$(window)
  .scroll(positionFooter)
  .resize(positionFooter);