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
      },
      error: function (result) {
        console.log("Something goes wrong, try again!");
      }
    })
  }
}