class ChiSquare {

  constructor(container) {
    this.container = container;
    this.validate = false;
    this.width = 0;
    this.height = 0;
  }

  setWidth(width) {
    this.width = parseInt(width);
  }

  setHeight(height) {
    this.height = parseInt(height);
  }

  createTable() {
    let table = `
      <table class="table table-responsive text-center">
        <thead class="thead-light">
        </thead>
        <tbody>
        </tbody>
      </table>`

    $(this.container).append(table);
  }


  drawTableHead() {
    $(this.container + ' .table thead').append(`<th scope="col">#</th>`);

    for (let i = 0; i < this.width; i++) {
      $(this.container + ' .table thead').append(`<th scope="col">column ${i}</th>`);
    }

    $(this.container + ' .table thead').append(`<th scope="col">Summary</th>`);
  }

  drawTableBody() {
    for (let i = 0; i < this.height + 1; i++) {


      if (i === this.height) {
        let row_summary = `<tr class="summary-row"></tr>`;
        $(this.container + ' .table tbody').append(row_summary);
        $('.summary-row').append('<th scope="row">Summary</th>');
      }
      else {
        let row = `<tr class="row-${i}"></tr>`;
        $(this.container + ' .table tbody').append(row);
      }

      for (let j = 0; j < this.width + 1; j++) {

        if (j === 0) {
          $(`${this.container} .row-${i}`).append(`<th scope="row">${i}</th>`)
        }

        if (i === this.height) {
          $('.summary-row').append(`<td class="summary">${this.generateSummaryInput(i, j)}</td>`);
        }
        else if (j === this.width) {
          $(`${this.container} .row-${i}`).append(`<td class="summary">${this.generateSummaryInput(i, j)}</td>`);
        }
        else {
          $(`${this.container} .row-${i}`).append(`<td>${this.generateInput(i, j)}</td>`);
        }

      }

    }
  }

  draw() {
    $(this.container).html('');
    this.createTable();
    this.drawTableHead();
    this.drawTableBody();
    $('.general-result').parent().addClass('general-result-wrapper');
    this.showCalcuateButton();
  }

  showCalcuateButton() {
    $('.calcuate').show();
  }

  generateInput(row, col) {
    return `<input type="number" min="0" class="form-control non-negative cell col line-${row} column-${col}" name="cell">`;
  }

  generateSummaryInput(row, col) {
    if (row === this.height && col === this.width) {
      return `<input type="number" class="form-control cell col summary-cell general-result" name="cell" readonly disabled>`;
    }
    else {
      return `<input type="number" class="form-control cell col summary-cell summary-line-${row} summary-column-${col}" name="cell" readonly disabled>`;
    }
  }

  showMessage(valid) {
    let message = '';
    if (valid) {
      message = '<div class="alert alert-success" role="alert">Validation successfull!</div>';
    }
    else {
      message = '<div class="alert alert-danger" role="alert">Fill all of the inputs!</div>';
    }

    $('.messages').html(message);
  }

  validateInputs() {
    let valid = true;
    $('.cell:not(.summary-cell)').each((index, elem) => {
      if (!$(elem).val()) {
        return valid = false;
      }
    });
    this.showMessage(valid);
  }

  sumAll(selector) {
    let sum = 0;
    $(selector).each(function () {
      sum += Number($(this).val());
    });
    return sum;
  }

  calculateRowColSum() {
    let sumRow = 0;
    for (let i = 0; i < this.height; i++) {
      sumRow = this.sumAll(`.line-${i}`);
      $(`.summary-line-${i}`).val(sumRow);
    }

    let sumCol = 0;
    for (let i = 0; i < this.width; i++) {
      sumCol = this.sumAll(`.column-${i}`);
      $(`.summary-column-${i}`).val(sumCol);
    }
  }

  calcuateUserInput() {
    let sumAll = this.sumAll('.cell:not(.summary-cell)');
    $('.general-result').val(sumAll);
  }

  calacute() {
    this.validateInputs();
    this.calculateRowColSum();
    this.calcuateUserInput();
  }

  buildJSON() {
    let data = {};

    for (let i = 0; i < this.height; i++) {
      let rowArray = $(`.line-${i}`).map(function () {
        return parseFloat($(this).val());
      }).get();
      data[`row-${i}`] = rowArray;
    }

    for (let i = 0; i < this.height; i++) {
      let colArray = $(`.column-${i}`).map(function () {
        return parseFloat($(this).val());
      }).get();
      data[`column-${i}`] = colArray;
    }

    data["width"] = this.width;
    data["height"] = this.height;
    data["field_sum"] = $('.general-result').val();

    return JSON.stringify(data);
  }

  sendData() {
    let dataJSON = this.buildJSON();
    const path = '/chi-square/send-data';
    const render = new RenderHelper('.chi-result');
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