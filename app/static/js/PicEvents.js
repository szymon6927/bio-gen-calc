const pic = new PicH();
const validator = new Validation();

$('#type-of-marker').change(function () {
  let markerType = $(this).val();
  pic.setMarkerType(markerType);
  pic.display();

  positionFooter();
});

$('.generate-codominant').click(function () {
  let number = $('.alleles-number').val();
  pic.generateCodominantInputs(number);

  setTimeout(() => {
    validator.nonNegative()
  },500);

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