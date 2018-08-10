function renderPDF() {
  $('.cover').show();

  let container = $('.wrapper');

  // set value atribute for pdf redner
  container.find('input').each((index, elem) => {
    let inputValue = $(elem).val();
    $(elem).attr('value', inputValue)
  });

  container.find('input').each((index, elem) => {
    let inputValue = $(elem).val();
    $(elem).attr('value', inputValue)
  });

  let data = {};
  data['content'] = container.html();

  const path = '/generate-pdf';
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: path,
    data: JSON.stringify(data),
    success: function (result) {
      let downloadLink = document.getElementById('download-link');
      downloadLink.href = 'data:application/octet-stream;base64,' + result;

      downloadLink.click();
      $('.cover').hide();
    },
    error: function (request) {
      console.log("Error druring render", request);
    }
  });
}

$(document).on('click', '.render-to-pdf', function (e) {
  e.preventDefault();
  renderPDF();
});