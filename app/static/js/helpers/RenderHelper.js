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
        '<>': 'div', 'class':'row result-score', 'html': [
          {
            '<>': 'span', 'class': 'col-md-6 col-sm-6 col-12 text-left result-name',
            'html': '<div>${name} =</div>',
          },
          {
            '<>': 'span', 'class': 'col-md-6 col-sm-6 col-12 text-left result-value',
            'html': '<div>${value}</div>',
          }
        ]
      };

      $(this.container).html(template);
      $(this.container + ' .card-body').json2html(result.data, transform);
  }

  errorBlock(request) {
    let errMsg = '';
    if (request && request.status === 409) {
      errMsg = `<div>Error message: ${request.responseText}</div>`;
    }

    let template = `<div class="alert alert-danger mt-4 mb-3" role="alert">
      <div>Something goes wrong, Try again!</div>
      ${errMsg}
    </div>`;

    $(this.container).html(template);
  }
}