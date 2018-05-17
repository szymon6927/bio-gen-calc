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
      <table class="table">
        <thead>
        </thead>
        <tbody>
        </tbody>
      </table>`

    $(this.container).append(table);
  }


  drawTableHead() {
    $(this.container + ' .table thead').append(`<th scope="col">#</th>`);

    for(let i = 0; i < this.width; i++) {
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
          $(`.row-${i}`).append(`<th scope="row">${i}</th>`)
        }

        if (i === this.height) {
          $('.summary-row').append(`<td class="summary">${this.generateSummaryInput(i, j)}</td>`);
        }
        else if (j === this.width) {
          $(`.row-${i}`).append(`<td class="summary">${this.generateSummaryInput(i, j)}</td>`);
        }
        else {
          $(`.row-${i}`).append(`<td>${this.generateInput(i, j)}</td>`);
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
    return `<input type="text" class="cell col line-${row} column-${col}" name="cell">`;
  }

  generateSummaryInput(row, col) {
    if (row === this.height && col === this.width) {
      return `<input type="text" class="cell col summary-cell general-result" name="cell" readonly>`;
    }
    else {
      return `<input type="text" class="cell col summary-cell summary-line-${row} summary-column-${col}" name="cell" readonly>`;
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
    $('.cell:not(.summary-cell)').each( (index, elem) => {
      if ( !$(elem).val() ) {
        console.log("return false");
        valid = false;
        return false;
      }
    });
    this.showMessage(valid);
  }

  sumAll(selector) {
    let sum = 0;
    $(selector).each( function() {
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
}