class GeneticDistance {
  constructor() {
    this.container = '';
    this.taxonNumber = 0;
    this.locusNumber = 0;
    this.locusObj = {};
  }

  setContainer(container) {
    this.container = container;
  }

  setLocusNumber(count) {
    this.locusNumber = parseInt(count);
  }

  setTaxonNumber(count) {
    this.taxonNumber = parseInt(count);
  }

  setLocusObject() {
    for (let i = 0; i < this.locusNumber; i++) {
      this.locusObj[i] = parseInt($(`#locus-${i}`).val());
    }
    console.log(this.locusObj);
  }

  generateAllelesInput(count) {
    const wrapper = '.alleles-wrapper';

    $(wrapper).html('');
    count = parseInt(count);
    for (let i = 0; i < count; i++) {
      let input = `<div class="form-group">
        <label for="locus-${i}">number of alleles in locus-${i}</label>
        <input type="number" class="form-control" id="locus-${i}">
      </div>`;

      $(wrapper).append(input);
    }
    let button = `<button type="submit" class="btn btn-block btn-success generate-table">Generate table</button>`;
    $(wrapper).append(button);
  }

  drawTableScheme() {
    let table = `<table class="table table-responsive text-center">
      <thead class="thead-light"></thead>
      <tbody></tbody>
      </table>`;

    $(this.container).append(table);
  }

  drawTableHead() {
    let tableHead = `<tr><th rowspan="2">Locus</th><th rowspan="2">Allel</th></tr><tr class="taxon-head-count"></tr>`;

    $(`${this.container} thead`).append(tableHead);

    for (let i = 0; i < this.taxonNumber; i++) {
      $(`${this.container} .taxon-head-count`).append(`<th>${i}</th>`);
    }
  }

  drawTableBody() {
    for (let key in this.locusObj) {
      if (this.locusObj.hasOwnProperty(key)) {
        console.log(key + " -> " + this.locusObj[key]);

        let tr = `<tr class="group-name"><th scope="row" rowspan="${this.locusObj[key] + 1}">G-${key}</th></tr>`;
        $(`${this.container} tbody`).append(tr);

        for (let i = 0; i < this.locusObj[key]; i++) {
          let line = `<tr class="group g-${key} line-${i}"></tr>`;
          $(`${this.container} tbody`).append(line);
          this.drawInputs(key, i);
        }
      }
    }
  }

  drawInputs(key, alleleNumber) {
    $(`.g-${key}.line-${alleleNumber}`).append(`<td>${alleleNumber}</td>`);
    let inputs = '';
    for (let i = 0; i < this.taxonNumber; i++) {
      inputs += '<td><input type="number" class="form-control cell col" name="cell"></td>';
    }
    $(`.g-${key}.line-${alleleNumber}`).append(inputs);
  }


  generateTable() {
    $(`${this.container}`).html('');
    this.drawTableScheme();
    this.drawTableHead();
    this.drawTableBody();
  }
}