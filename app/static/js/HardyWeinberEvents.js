const hw = new HardyWeinber();

$('.calcuate-hw').click(function () {
  let ho = $('#ho').val();
  let he = $('#he').val();
  let rho = $('#rho').val();
  let alfa = $('#alfa').val();

  if (!hw.validateData(ho, he, rho)) {
    showModal('Please insert int values');
    return false;
  }

  if ((ho == 0 && he == 0) || (he == 0 && rho == 0)) {
    showModal('Incorrect validation, more than two values are equal to 0 !');
    return false;
  }


  hw.setHo(ho);
  hw.setHe(he);
  hw.setRho(rho);
  hw.setAlpha(alfa);


  hw.sendData();

  setTimeout(() => {
    goToByScroll('.hw-results');
  }, 300)
});

$('.form-control').keypress(function (e) {
  if (e.which == 13) {
    $('.calcuate-hw').trigger('click');
    return false;    //<---- Add this line
  }
});

$(document).on('click', '.render-to-pdf', function () {
  console.log("render pdf");
  let container = $('.hardy-weinberg').html();

  let data = {};
  data['content'] = container;

  data = JSON.stringify(data);

  const path = 'http://127.0.0.1:5000/generate-pdf';
  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: path,
    data: data,
    success: function (result) {
      console.log(result);
      // create a download anchor tag
      // var downloadLink      = document.createElement('a');
      // downloadLink.target   = '_blank';
      // downloadLink.download = 'example.pdf';

      // // convert downloaded data to a Blob
      // var blob = new Blob([encodeURI(result)], { type: 'application/pdf' });

      // // create an object URL from the Blob
      // var URL = window.URL || window.webkitURL;
      // var downloadUrl = URL.createObjectURL(blob);

      // // set object URL as the anchor's href
      // downloadLink.href = downloadUrl;

      // // append the anchor to document body
      // document.body.append(downloadLink);

      // // fire a click event on the anchor
      // downloadLink.click();

      // // cleanup: remove element and revoke object URL
      // document.body.removeChild(downloadLink);
      // URL.revokeObjectURL(downloadUrl);

      // let pdfIframe = "<iframe width='100%' height='100%' src='data:application/pdf;base64, " + encodeURI(result) + "'></iframe>";
      // $('.hw-results').append(pdfIframe);

      let pdfWindow = window.open("")
pdfWindow.document.write("<iframe width='100%' height='100%' src='data:application/pdf;base64, " + encodeURI(result) + "'></iframe>")
    },
    error: function (request) {
      console.log("Error druring render", request);
    }
  });
});