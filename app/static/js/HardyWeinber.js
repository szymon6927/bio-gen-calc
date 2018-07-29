class HardyWeinber {
  constructor() {
    this.ho = 0;
    this.he = 0;
    this.rho = 0;
    this.alpha = 0;
  }

  setHo(ho) {
    this.ho = parseInt(ho);
  }

  setHe(he) {
    this.he = parseInt(he);
  }

  setRho(rho) {
    this.rho = parseInt(rho);
  }

  setAlpha(alpha) {
    this.alpha = parseFloat(alpha);
  }

  isInt(value) {
    let x;
    return isNaN(value) ? !1 : (x = parseFloat(value), (0 | x) === x);
  }

  validateData(ho, he, rho) {
    return this.isInt(ho) && this.isInt(he) && this.isInt(rho)
  }

  buildJSON() {
    let data = {};

    data["ho"] = this.ho;
    data["he"] = this.he;
    data["rho"] = this.rho;
    data["alfa"] = this.alpha;

    return JSON.stringify(data);
  }

  sendData() {
    const path = 'hardy-weinber/send-data';
    let dataJSON = this.buildJSON();
    console.log(dataJSON);

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Successfull!");

        let transform = {
          '<>': 'div', 'class':'row result-score', 'html': [
            {
              '<>': 'span', 'class': 'col-sm-6 col-xs-12 text-left result-name',
              'html': '<div>${name} =</div>',
            },
            {
              '<>': 'span', 'class': 'col-sm-6 col-xs-12 text-left result-value',
              'html': '<div>${value}</div>',
            }
          ]
        };

        $('.hw-results').show();
        $('.hw-results .card-body').json2html(result.data, transform);
      },
      error: function (result) {
        console.log("Something goes wrong, try again!", result);

        let template = `<div class="alert alert-danger" role="alert">
          Something goes wrong, Try again!
        </div>`;

        $('.hw-results').show();
        $('.hw-results').html(template);
      }
    })
  }
}