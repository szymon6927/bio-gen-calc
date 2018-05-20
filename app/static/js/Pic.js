class PicH {
  constructor() {
    this.markerType = '';
  }

  setMarkerType(markerType) {
    this.markerType = markerType;
  }

  display() {
    $('.codominant-wrapper, .dominant-wrapper').hide();
    $(`.${this.markerType}-wrapper`).show();
  }

  generateCodominantInputs(count) {
    $('.inputs-wrapper').html('');
    count = parseInt(count);
    for (let i = 0; i < count; i++) {
      let input = `<div class="form-group">
        <label for="allele-${i}">allele-${i}</label>
        <input type="number" class="form-control allele-input" id="allele-${i}">
      </div>`;

      $('.inputs-wrapper').append(input);
    }
  }

  buildCodominantJSON() {
    let data = {};
    let count = $('.allele-input').length;

    for (let i = 0; i < count; i++) {
      data[`allele-${i}`] = $(`#allele-${i}`).val();
    }

    data["count"] = count;

    return JSON.stringify(data);
  }

  buildDominantJSON() {
    let data = {};

    let amplifiedMarker = $('#amplified-marker').val();
    let absecnceMarker = $('#absecnce-marker').val();

    data["amplified_marker"] = amplifiedMarker;
    data["absecnce_marker"] = absecnceMarker;

    return JSON.stringify(data);
  }

  sendCodominant() {
    let dataJSON = this.buildCodominantJSON();
    console.log(dataJSON);
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/sendCodominant",
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Successfull!");
        console.log(result.data);

        let info = '';

        for (let key in result.data) {
          if (result.data.hasOwnProperty(key)) {
            console.log(key + " -> " + result.data[key]);
            let name = key.replace("_", " ");
            info += `<div class="row result-score">
              <span class="col-sm-6 col-xs-12 result-name">${name} = </span> 
              <input class="col-sm-6 col-xs-12 result-value" type="text" value="${result.data[key]}" />
            </div>`
          }
        }

        let template = `<div class="card text-center">
          <div class="card-header">Results:</div>
          <div class="card-body">
            <div class="card-text text-left">${info}</div>
          </div>
        </div>`;


        $('.codominant-result').html(template);
      },
      error: function (result) {
        console.log("Something goes wrong, try again!");

        let template = `<div class="alert alert-danger" role="alert">
          Something goes wrong, Try again!
        </div>`;

        $('.codominant-result').html(template);
      }
    })
  }

  sendDominant() {
    let dataJSON = this.buildDominantJSON();
    console.log(dataJSON);
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/sendDominant",
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Successfull!");
        console.log(result.data);

        let info = '';

        for (let key in result.data) {
          if (result.data.hasOwnProperty(key)) {
            console.log(key + " -> " + result.data[key]);
            let name = key.replace("_", " ");
            info += `<div class="row result-score">
              <span class="col-sm-6 col-xs-12 result-name">${name} = </span> 
              <input class="col-sm-6 col-xs-12 result-value" type="text" value="${result.data[key]}" />
            </div>`
          }
        }

        let template = `<div class="card text-center">
          <div class="card-header">Results:</div>
          <div class="card-body">
            <div class="card-text text-left">${info}</div>
          </div>
        </div>`;


        $('.dominant-result').html(template);
      },
      error: function (result) {
        console.log("Something goes wrong, try again!");

        let template = `<div class="alert alert-danger" role="alert">
          Something goes wrong, Try again!
        </div>`;

        $('.dominant-result').html(template);
      }
    })
  }
}