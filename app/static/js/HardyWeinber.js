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
    const render = new RenderHelper('.hw-results');
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
        render.successBlock(result);
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);
        render.errorBlock(request);
      }
    })
  }
}