const moduleSections = '.raw-sequences, .upload-sequences, .sequences-form-genebank';

$('#type-of-data').change(function () {
  $(moduleSections).hide();
  let type = $(this).val();
  $(`.${type}`).show();
});