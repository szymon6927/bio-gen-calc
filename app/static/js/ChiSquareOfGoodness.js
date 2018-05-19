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
      <table class="table">
        <thead>
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
    return `<td><input type="text" class="form-control cell col ${type} column-${col}" name="cell"></td>`;
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
      success: function (data) {

        let result = `
        <div class="alert alert-dark" role="alert">
          <div>chi2 ${data.data["chi2_standard"]}</div>
          <div>chi2 with Yats corection ${data.data["chi2_yats"]}</div>
          <div>degrees of freedom ${data.data["dof"]}</div>
          <div>p ${data.data["p_standard"]}</div>
          <div>p with Yats corection ${data.data["p_yats"]}</div>
        </div>`;

        $('.chi-goodness-result').html(result)
        $('.summary-observed').val(data.data["sum_observed"]);
        $('.summary-expected').val(data.data["sum_expected"]);
      },
      error: function (data) {
        $('.chi-goodness-result').html('Something goes wrong! Try again!')
      }
    })
  }
}