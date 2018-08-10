const pic = new PicH();
const validator = new Validation();

$('#type-of-marker').change(function () {
  let markerType = $(this).val();

  $('#type-of-marker option').removeAttr('selected');
  $(`#type-of-marker option[value='${markerType}']`).attr("selected","selected");

  pic.setMarkerType(markerType);
  pic.display();

  setTimeout(() => {
    positionFooter();
  }, 300)
});

$('.generate-codominant').click(function () {
  let number = $('.alleles-number').val();
  pic.generateCodominantInputs(number);

  setTimeout(() => {
    validator.nonNegative()
  }, 500);

  $('.calcuate-codominant').show();

  goToByScroll('.inputs-wrapper');
});

$('.calcuate-codominant').click(function () {
  pic.sendCodominant();
  goToByScroll('.codominant-result');
});

$('.calcuate-dominant').click(function () {
  pic.sendDominant();
  goToByScroll('.dominant-result');
});

$(document).on('keypress', '.amplified-marker, .absecnce-marker', function (e) {
  if (e.which == 13) {
    $('.calcuate-dominant').trigger('click');
    return false;
  }
});

$(document).on('keypress', '.alleles-number', function (e) {
  if (e.which == 13) {
    $('.generate-codominant').trigger('click');
    $('.allele-input').first().focus();
    return false;
  }
});

$(document).on('keypress', '.allele-input', function (e) {
  if (e.which == 13) {
    $('.calcuate-codominant').trigger('click');
    return false;
  }
});



