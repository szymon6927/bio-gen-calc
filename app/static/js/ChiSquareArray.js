class ChiSquareArray {

  constructor(width, height, container) {
    this.width = parseInt(width);
    this.height = parseInt(height);
    this.container = container;
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

    for(let i = 0; i < this. width; i++) {
      $(this.container + ' .table thead').append(`<th scope="col">column ${i}</th>`);
    }

    $(this.container + ' .table thead').append(`<th scope="col">Summary</th>`);
  }

  drawTableBody() {
    for (let i = 0; i < this.height + 1; i++) {
      let row = `<tr class="row-${i}"></tr>`;
      $(this.container + ' .table tbody').append(row);

      if (i == this.height) {
        let row_summary = `<tr class="summary-row"></tr>`;
        $(this.container + ' .table tbody').append(row_summary);
      }

      for (let j = 0; j < this.width + 1; j++) {
        // if (j == this.width) {
        //   $(`.row-${i}`).append(`<td>${this.generateSummaryInput(i, j)}</td>`)
        // }

        if (j === 0) {
          $(`.row-${i}`).append(`<th scope="row">${i}</th>`)
        }

        if (j === this.width && i == this.height) {
          $(`.row-${i}`).append(`<td>${this.generateSummaryInput(i, j)}</td>`)
        }
        else {
          $(`.row-${i}`).append(`<td>${this.generateInput(i, j)}</td>`)
        }


      }

    }
  }

  draw() {
    $(this.container).html('');
    this.createTable();
    this.drawTableHead();
    this.drawTableBody();
  }

  generateInput(row, col) {
    return `<input type="text" class="cell col line-${row} column-${col}" name="cell">`;
  }

  generateSummaryInput(row, col) {
    return `<input type="text" class="cell col summary-${row}-${col}" name="cell">`;
  }
}