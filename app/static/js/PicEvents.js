const pic = new PicH();

$('#type-of-marker').change(function () {
  let markerType = $(this).val();
  console.log(markerType);
  pic.setMarkerType(markerType);
  pic.display();
});

$('.generate-codominant').click(function () {
  let number = $('.alleles-number').val();
  pic.generateCodominantInputs(number);
});

$('.calcuate-codominant').click(function () {
  pic.sendCodominant();
});

$('.calcuate-dominant').click(function () {
  pic.sendDominant();
});