const geneticDistance = new GeneticDistance();
geneticDistance.setContainer('.genetic-distance-table')

$('.alleles-inputs-generate').click(function () {
  let count = $('.locus-number').val();
  geneticDistance.generateAllelesInput(count);
});


$(document).on('click', '.generate-table', function () {
  console.log("Generate table");
  let taxonNumber = $('#taxon-number').val();
  let locusNumber = $('#locus-number').val();

  geneticDistance.setTaxonNumber(taxonNumber);
  geneticDistance.setLocusNumber(locusNumber);
  geneticDistance.setLocusObject();
  geneticDistance.generateTable();
});

$('.calcuate-distance').click(function () {
  // geneticDistance.buildJSON();
  geneticDistance.sendData();
})

