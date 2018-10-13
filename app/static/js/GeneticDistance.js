// in future import showModal form './utils'

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

  validateColumnSum() {
    $('.genetic-distance-table').find('input').removeClass('is-invalid');
    const possibleResults = [...Array(this.locusNumber + 1).keys()];

    for (let i = 0; i < this.taxonNumber; i++) {
      let columnValue = $(`.column-${i}`).map(function () {
        return parseFloat($(this).val());
      }).get();

      let columnSum = Number(columnValue.reduce((a, b) => a + b).toFixed(2));

      if (!possibleResults.includes(columnSum)) {
        $(`.column-${i}`).addClass('is-invalid');
        showModal(`In column ${i} values are incorrect`);
        return false;
      }
    }

    return true;
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

    $('.generate-table').show();
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
      inputs += `<td><input type="number" min="0" max="1" step="0.01" class="form-control column-${i} 
      cell non-negative float01" name="cell"><div class="invalid-feedback">Value range 0.0 - 1.0</div></td>`;
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

  // matrixDesc() {
  //   let topWidth = $('.MathJax_SVG').last().width() + "px";
  //   let topDesc = `<div class="top-desc" style="width: ${topWidth};"></div>`;
  //   $(topDesc).insertAfter('.MathJax_Preview');

  //   for (let i = 0; i < this.taxonNumber - 1; i++) {
  //     let div = `<div class="top-desc-item">${i}</div>`;
  //     $('.top-desc').append(div);
  //   }


  //   let fullWidth = $('.matrix-latex').width();
  //   let leftPos = (fullWidth / 2) - $('.MathJax_CHTML').last().width() + 70 + "px";
  //   let topPos = $('.matrix-latex').height() - $('.top-desc').height() - $('.MathJax_CHTML').last().height() - 5 + "px";
  //   let leftDesc = `<ul class="left-desc" style="left: ${leftPos}; top: ${topPos}"></ul>`;
  //   $(leftDesc).insertAfter('.top-desc');

  //   for (let i = 1; i < this.taxonNumber; i++) {
  //     $('.left-desc').append(`<li>${i}</li>`)
  //   }

  // }

  renderPDFButton() {
    let date = moment().format('DD/MM/YYYY-hh:mm');

    let pdfRender = `<div class="btn btn-secondary render-to-pdf">
                        <i class="fas fa-file-pdf"></i>
                        <span>Save results to pdf</span>
                    </div>
                    <a id="download-link" download="results-${date}.pdf" style="display:none;" />`;

    $('.pdf-wrapper').html(pdfRender);
  }

  sendData() {
    let dataJSON = this.buildJSON();
    console.log("dataJSON: ", dataJSON);
    const path = '/genetic-distance/send-data-distance';
    const render = new RenderHelper('.genetic-distance-results .error');
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      cache: false,
      success: (res) => {
        console.log("Succesfull");
        $('.genetic-distance-results .error').hide();
        $('.genetic-distance-results').show();
        $('.genetic-distance-results .success').show();

        // let matrixImg = `<p class="matrix-latex">${res.data.matrix_latex}</p>`;
        let dendroImg = `<img class="img-fluid" src="data:image/png;base64,${res.data.dendro_base64}">`;
        $('.matrix-wrapper').html(res.data.matrix_latex);
        $('.dendrogram-wrapper').html(dendroImg);

        // setTimeout(() => {
        //   MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        // }, 500);

        setTimeout(() => {
          // this.matrixDesc();
          $('.cover').hide();
          goToByScroll('.genetic-distance-results');
        }, 2000);

        this.renderPDFButton()
      },
      error: (request) => {
        $('.cover').hide();
        $('.genetic-distance-results .row.success').hide();
        console.log("Something goes wrong, try again!", request);
        render.errorBlock(request);
      }
    })
  }
}