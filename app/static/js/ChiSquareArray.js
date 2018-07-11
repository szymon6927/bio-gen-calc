class ChiSquareArray {

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
      return `<input type="number" class="form-control cell col summary-cell general-result" name="cell" readonly>`;
    }
    else {
      return `<input type="number" class="form-control cell col summary-cell summary-line-${row} summary-column-${col}" name="cell" readonly>`;
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
        console.log("return false");
        valid = false;
        return false;
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
    console.log("run calculating");
    this.calculateRowColSum();
    this.calcuateUserInput();
  }

  buildJSON() {
    let data = {};

    for (let i = 0; i < this.height; i++) {
      let rowArray = $(`.line-${i}`).map(function () {
        return $(this).val();
      }).get();
      data[`row-${i}`] = rowArray;
    }

    for (let i = 0; i < this.height; i++) {
      let colArray = $(`.column-${i}`).map(function () {
        return $(this).val();
      }).get();
      data[`column-${i}`] = colArray;
    }

    data["width"] = this.width;
    data["height"] = this.height;
    data["field_sum"] = $('.general-result').val();

    let dataJSON = JSON.stringify(data);

    return dataJSON;
  }

  sendData() {
    let dataJSON = this.buildJSON();
    const path = '/chi-square/send-data';
    console.log(dataJSON);
    console.log($.parseJSON(dataJSON))
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Succesfull");
        console.log(result.data);

        let info = '';

        for (let key in result.data) {
          if (result.data.hasOwnProperty(key)) {
            console.log(key + " -> " + result.data[key]);
            if (key !== 'yule' && key !== 'crammer') {
              info += `<div class="row result-score">
                <span class="col-sm-6 col-xs-12 result-name">${converterName(key)} = </span> 
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


        $('.chi-result').html(template)
      },
      error: function (data) {
        console.log(data);

        let template = `<div class="alert alert-danger" role="alert">
          Something goes wrong, Try again!
        </div>`;

        $('.chi-result').html(template)
      }
    })
  }
}