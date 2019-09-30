"use strict";

class HardyWeinber extends AppModule {
  constructor() {
    super();
    this.ho = 0;
    this.he = 0;
    this.rho = 0;
    this.alpha = 0;
    this.result = Object;
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

  getResult() {
    return this.result;
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
    const path = 'hardy-weinberg/send-data';
    let dataJSON = this.buildJSON();

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: (result) => {
        console.log("Successful!");
        render.successBlock(result);

        this.setResult(result);
        this.extendObjectToSave({'customer_input': dataJSON})
      },
      error: function (request) {
        console.log("Something went wrong, try again!", request);
        render.errorBlock(request);
      }
    })
  }
}
