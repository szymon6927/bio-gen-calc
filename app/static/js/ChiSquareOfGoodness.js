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
      <table class="table table-responsive text-center">
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
        $(this.container + ' .table thead').append(`<th scope="col">Group ${i}</th>`);
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
      return `<td class="summary"><input type="number" class="form-control cell col ${type} column-${col}" name="cell" readonly disabled></td>`;
    }
    else {
      return `<td><input type="number" min="0" class="form-control non-negative cell col ${type} column-${col}" name="cell"></td>`;
    }
  }

  compareArrSum(observedArr, expectedArr) {
    let observedSum = observedArr.reduce((a, b) => a + b, 0).toFixed(2);
    let expectedSum = expectedArr.reduce((a, b) => a + b, 0).toFixed(2);

    $('.summary-observed').val(observedSum);
    $('.summary-expected').val(expectedSum);

    if (observedSum !== expectedSum) {
      let info = `<div class="alert alert-warning mt-3" role="alert">Expected values doesn't equal observed</div>`;
      $('.chi-goodness-info').html(info);
    }
    else {
      $('.chi-goodness-info').html('');
    }
  }

  buildJSON() {
    let data = {};
    let observedRow = $('.observed').map(function () {
      return parseFloat($(this).val());
    }).get();

    let expectedRow = $('.expected').map(function () {
      return parseFloat($(this).val());
    }).get();

    data["observed"] = observedRow;
    data["expected"] = expectedRow;

    this.compareArrSum(observedRow, expectedRow);

    return JSON.stringify(data);
  }

  sendData() {
    let dataJSON = this.buildJSON();
    const path = '/chi-square/send-data-goodness';
    const render = new RenderHelper('.chi-goodness-result');
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Succesfull");

        render.successBlock(result);
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);
      }
    })
  }
}