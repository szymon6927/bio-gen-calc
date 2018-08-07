// in future import showModal form './utils'

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

  validateCodominant() {
    let valid = true;
    $('.allele-input').each(function () {
      let val = $(this).val();
      if (val == 0) {
        return valid = false;
      }
    });
    return valid;
  }

  showMessage(valid) {
    let message = '';
    if (valid) {
      message = '<div class="alert alert-success" role="alert">Validation successfull!</div>';
    }
    else {
      message = '<div class="alert alert-danger" role="alert">More than 0 number required</div>';
    }

    $('.codominant-messages').html(message);
  }

  generateCodominantInputs(count) {
    $('.inputs-wrapper').html('');
    count = parseInt(count);
    for (let i = 0; i < count; i++) {
      let input = `<div class="form-group">
        <label for="allele-${i}">allele-${i}</label>
        <input type="number" min="0" class="form-control non-negative allele-input" id="allele-${i}">
      </div>`;

      $('.inputs-wrapper').append(input);
    }
  }

  buildCodominantJSON() {
    let data = {};
    let count = $('.allele-input').length;

    for (let i = 0; i < count; i++) {
      data[`allele-${i}`] = Number($(`#allele-${i}`).val());
    }

    data["count"] = count;

    return JSON.stringify(data);
  }

  buildDominantJSON() {
    let data = {};

    let amplifiedMarker = $('#amplified-marker').val();
    let absecnceMarker = $('#absecnce-marker').val();

    if (amplifiedMarker && absecnceMarker) {
      data["amplified_marker"] = Number(amplifiedMarker);
      data["absecnce_marker"] = Number(absecnceMarker);
    }
    else {
      showModal('Fill number of amplified marker or number of absecnce marker')
      return false
    }

    return JSON.stringify(data);
  }

  sendCodominant() {
    let valid = this.validateCodominant();
    this.showMessage(valid);

    let dataJSON = this.buildCodominantJSON();

    const render = new RenderHelper('.codominant-result');
    const path = 'pic/send-codominant';
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Successfull!");

        render.successBlock(result);
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);
      }
    })
  }

  sendDominant() {
    let dataJSON = this.buildDominantJSON();

    if (!dataJSON) {
      // break if all data not filled in inputs
      return false
    }

    const path = '/pic/send-dominant';
    const render = new RenderHelper('.dominant-result');
    console.log(dataJSON);
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Successfull!");

        render.successBlock(result);
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);
      }
    })
  }
}