function renderPDF() {
  $('.cover').show();

  const container = document.querySelector('.wrapper');
  const inputs = container.querySelectorAll('input');
  const textareas = container.querySelectorAll('textarea');

  inputs.forEach((elem) => {
    elem.setAttribute('value', elem.value);
  });

  textareas.forEach((elem) => {
    elem.innerHTML = elem.value;
    elem.style.height = `${elem.scrollHeight}px`;
  })

  let data = {};
  data['content'] = container.innerHTML;

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