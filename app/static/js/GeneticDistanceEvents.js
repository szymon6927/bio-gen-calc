const geneticDistance = new GeneticDistance();
const validator = new Validation()

geneticDistance.setContainer('.genetic-distance-table')

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

