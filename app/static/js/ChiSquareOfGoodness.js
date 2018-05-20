class ChiSquareOfGoodness {
  constructor(container) {
    this.container = container;
    this.width = 0;
  }

  setWidth(width) {
    this.width = parseInt(width);
  }

  createTable() {
    let table = `
      <table class="table text-center">
        <thead class="thead-light">
        </thead>
        <tbody>
          <tr class="row-0">
            <th scope="row">Observed</th>
          </tr>
          <tr class="row-1">
            <th scope="row">Expected</th>
          </tr>
        </tbody>
      </table>`;

    $(this.container).append(table);
  }

  drawTableHead() {
    $(this.container + ' .table thead').append(`<th scope="col">#</th>`);

    for (let i = 0; i < this.width + 1; i++) {
      if (i === this.width) {
        $(this.container + ' .table thead').append(`<th scope="col">Summary</th>`);
      }
      else {
        $(this.container + ' .table thead').append(`<th scope="col">gp ${i}</th>`);
      }
    }
  }

  drawTableBody() {
    for (let i = 0; i < this.width + 1; i++) {
      if (i === this.width) {
        $(this.container + ' .row-0').append(this.generateInput(i, "summary-observed"));
        $(this.container + ' .row-1').append(this.generateInput(i, "summary-expected"));
      }
      else {
        $(this.container + ' .row-0').append(this.generateInput(i, "observed"));
        $(this.container + ' .row-1').append(this.generateInput(i, "expected"));
      }
    }
  }

  draw() {
    $(this.container).html('');
    this.createTable();
    this.drawTableHead();
    this.drawTableBody();
    $('.calcuate-goodness').show();
  }

  generateInput(col, type) {
    if (type === "summary-observed" || type === "summary-expected") {
      return `<td class="summary"><input type="number" class="form-control cell col ${type} column-${col}" name="cell" readonly></td>`;
    }
    else {
      return `<td><input type="number" class="form-control cell col ${type} column-${col}" name="cell"></td>`;
    }
  }

  buildJSON() {
    let data = {}
    let observedRow = $('.observed').map(function () {
      return $(this).val();
    }).get();

    let expectedRow = $('.expected').map(function () {
      return $(this).val();
    }).get();

    data["observed"] = observedRow;
    data["expected"] = expectedRow;

    let dataJSON = JSON.stringify(data);
    return dataJSON;
  }

  sendData() {
    let dataJSON = this.buildJSON();
    console.log(dataJSON)
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/sendDataGoodness",
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        let info = '';

        for (let key in result.data) {
          if (result.data.hasOwnProperty(key)) {
            console.log(key + " -> " + result.data[key]);
            if (key !== 'sum_observed' || key !== 'sum_expected') {
              let name = key.replace("_", " ");
              info += `<div class="row result-score">
                <span class="col-sm-6 col-xs-12 result-name">${name} = </span> 
                <input class="col-sm-6 col-xs-12 result-value" type="text" value="${result.data[key]}" />
              </div>`
            }
          }
        }

        let template = `<div class="card text-center">
          <div class="card-header">Results:</div>
          <div class="card-body">
            <div class="card-text text-left">${info}</div>
          </div>
        </div>`

        $('.chi-goodness-result').html(template)
        $('.summary-observed').val(result.data["sum_observed"]);
        $('.summary-expected').val(result.data["sum_expected"]);
      },
      error: function (data) {
        $('.chi-goodness-result').html('Something goes wrong! Try again!')
      }
    })
  }
}