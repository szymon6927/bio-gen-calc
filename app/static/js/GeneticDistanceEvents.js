const geneticDistance = new GeneticDistance();
geneticDistance.setContainer('.genetic-distance-table')

$('.alleles-inputs-generate').click(function () {
  let taxonNumber = $('#taxon-number').val();
  let count = $('#locus-number').val();
  if (taxonNumber && count) {
    geneticDistance.generateAllelesInput(count);
  }
  else {
    showModal('Please, fill all inputs!')
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
  }
  else {
    showModal('Please, fill all number of alleles inputs!')
  }
});

$('.calcuate-distance').click(function () {
  const validator = new Validation()
  if (validator.floatBetween01('.float01')) {
    geneticDistance.sendData();
    $('.cover').show()
  }
})

