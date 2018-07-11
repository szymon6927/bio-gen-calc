const pic = new PicH();

$('#type-of-marker').change(function () {
  let markerType = $(this).val();
  pic.setMarkerType(markerType);
  pic.display();
});

$('.generate-codominant').click(function () {
  let number = $('.alleles-number').val();
  pic.generateCodominantInputs(number);
  
  setTimeout(() => {
    validateNegative()
  },500)
});

$('.calcuate-codominant').click(function () {
  pic.sendCodominant();
});

$('.calcuate-dominant').click(function () {
  pic.sendDominant();
});