"use strict";

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

  $('.calculate-codominant').show();

  goToByScroll('.inputs-wrapper');
});

$('.calculate-codominant').click(function () {
  pic.sendCodominant();
  goToByScroll('.codominant-result');
});

$('.calculate-dominant').click(function () {
  pic.sendDominant();
  goToByScroll('.dominant-result');
});

$('.codominant-wrapper .save-calculation-form').submit(function(e) {
  e.preventDefault();
  pic.setContainer('.codominant-wrapper');
  pic.saveCalculation();
});

$('.dominant-wrapper .save-calculation-form').submit(function(e) {
  e.preventDefault();
  pic.setContainer('.dominant-wrapper');
  pic.saveCalculation();
});

$(document).on('keypress', '.amplified-marker, .absence-marker', function (e) {
  if (e.which == 13) {
    $('.calculate-dominant').trigger('click');
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
    $('.calculate-codominant').trigger('click');
    return false;
  }
});
