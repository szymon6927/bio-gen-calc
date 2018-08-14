const geneticDistance = new GeneticDistance();
const validator = new Validation();

geneticDistance.setContainer('.genetic-distance-table');

$('.alleles-inputs-generate').click(function () {
  let taxonNumber = $('#taxon-number').val();
  let count = $('#locus-number').val();
  if (taxonNumber && count) {
    geneticDistance.generateAllelesInput(count);
    goToByScroll('.alleles-wrapper');
  }
  else {
    showModal('Please, fill all inputs!');
  }
});


$(document).on('click', '.generate-table', function () {
  let taxonNumber = $('#taxon-number').val();
  let locusNumber = $('#locus-number').val();

  geneticDistance.setTaxonNumber(taxonNumber);
  geneticDistance.setLocusNumber(locusNumber);
  geneticDistance.setLocusObject();
  
  if (geneticDistance.validateLocusInputs()) {
    geneticDistance.generateTable();
    goToByScroll('.genetic-distance-table');
    setTimeout(() => {
      validator.nonNegative();
    },500)
  }
  else {
    showModal('Please, fill all number of alleles inputs!');
  }
});

$('.calcuate-distance').click(function () {
  if (validator.floatBetween01() && geneticDistance.validateColumnSum()) {
    geneticDistance.sendData();
    $('.cover').show();
  }
});

$('.genetic-distance select').change(function () {
  let value = $(this).val();

  $('.genetic-distance select option').removeAttr('selected');
  $(`.genetic-distance select option[value='${value}']`).attr("selected","selected");
});

$(document).on('keypress', '.taxon-number, .locus-number, #type-of-distance, #type-of-dendrogram', function (e) {
  if (e.which == 13) {
    $('.alleles-inputs-generate').trigger('click');
    $('.number-of-alleles input').first().focus();
    return false;
  }
});

$(document).on('keypress', '.number-of-alleles input', function (e) {
  if (e.which == 13) {
    $('.generate-table').trigger('click');
    $('.table .cell').first().focus();
    return false;
  }
});

$(document).on('keypress', '.table .form-control', function (e) {
  if (e.which == 13) {
    $('.calcuate-distance').trigger('click');
    return false;
  }
});




