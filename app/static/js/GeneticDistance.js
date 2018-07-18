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
      let locusVal = $(`#locus-${i}`).val()
      this.locusObj[i] = parseInt(locusVal);
    }
  }


  validateLocusInputs() {
    let valid = true;
    for (let i = 0; i < this.locusNumber; i++) {
      let locusVal = $(`#locus-${i}`).val()
      if (!locusVal) {
        return valid = false;
      }
    }
    return valid
  }

  generateAllelesInput(count) {
    const wrapper = '.alleles-wrapper';

    $(wrapper).html('');
    count = parseInt(count);
    for (let i = 0; i < count; i++) {
      let input = `<div class="form-group number-of-alleles">
        <label for="locus-${i}">number of alleles in locus-${i}</label>
        <input type="number" min="1" class="form-control" id="locus-${i}">
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
      inputs += `<td><input type="number" min="0" max="1" class="form-control column-${i} cell" name="cell"></td>`;
    }
    $(`.g-${key}.line-${alleleNumber}`).append(inputs);
  }


  generateTable() {
    $(`${this.container}`).html('');
    this.drawTableScheme();
    this.drawTableHead();
    this.drawTableBody();
    $('.calcuate-distance').show();
  }

  buildJSON() {
    console.log("JSON building");
    let data = {};
    data["taxon_number"] = $('#taxon-number').val();
    data["locus_number"] = $('#locus-number').val();
    data["type_of_distance"] = $('#type-of-distance').val();

    for (let i = 0; i < this.locusNumber; i++) {
      let gObject = {};
      let numberOfAlleles = $(`#locus-${i}`).val();
      gObject["nubmer_of_alleles"] = numberOfAlleles;

      for (let j = 0; j < numberOfAlleles; j++) {
        let gLocus = $(`.g-${i}.line-${j} input`).map(function () {
          return $(this).val();
        }).get();
        gObject[`alleles_${j}`] = gLocus;
      }
      data[`g_${i}`] = gObject;
    }

    return JSON.stringify(data);
  }

  buildJSON2() {
    console.log("json building 2")
    let data = {};

    data["taxon_number"] = $('#taxon-number').val();
    data["locus_number"] = $('#locus-number').val();
    data["type_of_distance"] = $('#type-of-distance').val();
    data["type_of_dendrogram"] = $('#type-of-dendrogram').val();
    data["number_of_alleles"] = $('.number-of-alleles input').map(function () {
      return parseFloat($(this).val());
    }).get();

    for (let i = 0; i < data["taxon_number"]; i++) {
      let columnValue = $(`.column-${i}`).map(function () {
        return parseFloat($(this).val());
      }).get();

      data[`column_${i}`] = columnValue
    }

    return JSON.stringify(data);
  }

  sendData() {
    let dataJSON = this.buildJSON2();
    console.log(dataJSON);
    const path = '/genetic-distance/send-data-distance';
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (res) {
        console.log("Succesfull");
        $('.genetic-distance-results').show()
        let matrixImg = `<p class="matrix-latex">${res.data.matrix_latex}</p>`;
        let dendroImg = `<img class="img-fluid" src="data:image/png;base64,${res.data.dendro_base64}">`;
        $('.matrix-wrapper').html(matrixImg)
        $('.dendrogram-wrapper').html(dendroImg)

        setTimeout(() => {
          MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }, 500)

        $('.cover').hide()

      },
      error: function (result) {
        console.log(result);
        $('.cover').hide()
      }
    })
  }
}