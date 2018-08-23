class RenderHelper {
  constructor(container) {
    this.container = container;
  }

  successBlock(result) {
    let template = `<div class="card text-center mt-5 mb-3">
        <div class="card-header">Results:</div>
        <div class="card-body">
          <div class="card-text text-left"></div>
        </div>
      </div>`;

    let transform = {
      '<>': 'div', 'class': 'row result-score', 'html': [
        {
          '<>': 'div', 'class': 'col-md-6 col-sm-6 col-12 text-left result-name',
          'html': '<div>${name} <span class="equal-char">=</span></div>',
        },
        {
          '<>': 'div', 'class': 'col-md-6 col-sm-6 col-12 text-left result-value',
          'html': '<div>${value}</div>',
        }
      ]
    };

    let pdfRender = `<div class="btn btn-secondary mt-3 render-to-pdf">
                          <i class="fas fa-file-pdf"></i>
                          <span>Save as PDF</span>
                      </div>`;

    let date = moment().format('DD/MM/YYYY-hh:mm');
    let downloadButton = `<a id='download-link' download='results-${date}.pdf' style="display:none;" /> `;

    $(this.container).html(template);
    $(this.container + ' .card-body').json2html(result.data, transform);
    $(this.container + ' .card-body').append(pdfRender);
    $(this.container + ' .card-body').append(downloadButton);
  }

  errorBlock(request) {
    if ($(this.container).is(":hidden")) {
      $(this.container).show();
    }

    let errMsg = '';
    if (request && (request.status === 409 || request.status === 400)) {
      errMsg = `<div><strong>Error message:</strong> ${request.responseText}</div>`;
    }

    let template = `<div class="alert alert-danger mt-4 mb-3" role="alert">
      <div>Something goes wrong, Try again!</div>
      ${errMsg}
    </div>`;

    $(this.container).html(template);
  }
}