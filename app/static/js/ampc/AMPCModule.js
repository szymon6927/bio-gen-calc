"use strict";

class AMPCModule extends AppModule {
  constructor() {
    super();
    this.ampcDataID = null;
  }

  setAmpcDataID(id) {
    this.ampcDataID = id;
  }

  getAmpcDataID() {
    return this.ampcDataID;
  }

  renderPreTrainResultsClassification(result) {
    const wrapper = $('.pre-train-results');
    let template = '';

    result.forEach((item, index) => {
      template += `
      <div>Model name: ${item.model_name}</div>
      <div>Accuracy: ${item.accuracy}</div>
      <div>cross_validate_score: ${item.cross_validate_score}</div>
      <div>${item.matrix_report}</div>`
    });

    wrapper.html(template);
  }

  renderPreTrainResultsRegression(result) {
    const wrapper = $('.pre-train-results');
    let template = '';

    result.forEach((item, index) => {
      template += `
      <div class="mb-3">
        <div>Model name: ${item.model_name}</div>
        <div>cross_validate_score: ${item.cross_validate_score}</div>
        <div>MAE: ${item.MAE}</div>
        <div>MSE: ${item.MSE}</div>
        <div>R2: ${item.R2}</div>
      </div>`
    });

    wrapper.html(template);
  }

  renderModelChoices(modelChoices) {
    const selectWraper = $('.user-model-choice select');
    let choices = '';

    modelChoices.forEach((item, index) => {
      choices += `
        <option value="${item.key}">${item.name}</option>
      `
    });

    selectWraper.html(choices);
  }

  preTrain() {
    $('.cover').show();
    const path = '/ampc/pre-train';
    const render = new RenderHelper('.pre-train-results');

    const fileInput = document.getElementById('data-file');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', file);

    const projectName = document.querySelector('#project-name').value;
    const modelType = document.querySelector('#model-type').value;
    const normalization = document.querySelector('#normalize-dataset').checked;

    formData.append('project_name', projectName);
    formData.append('model_type', modelType);
    formData.append('normalization', normalization);

    $.ajax({
      type: "POST",
      url: path,
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      success: (result) => {
        console.log("Succesfull");
        console.log(result);

        this.setAmpcDataID(result.data_id);

        if (modelType === "classification") {
          this.renderPreTrainResultsClassification(result.model_metrics);
        }
        else {
          this.renderPreTrainResultsRegression(result.model_metrics);
        }

        $('.user-model-choice').show();
        this.renderModelChoices(result.user_choices);

        $('.cover').hide();
      },
      error: (request) => {
        console.log("Something goes wrong, try again!", request);

        console.log(request);
        render.errorBlock(request);

        $('.cover').hide();
      }
    });
  }

  buildTrainJSON() {
    let data = {};

    data['selected_model'] = document.querySelector('.user-model-choice select').value;
    data['data_id'] = this.getAmpcDataID();

    return JSON.stringify(data);
  }

  train() {
    $('.cover').show();
    const path = '/ampc/train';
    const dataJSON = this.buildTrainJSON();
    const render = new RenderHelper('.train-errors');

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: (result) => {
        console.log("Successfull!");
        console.log(result);
        $('.cover').hide();
        $('.train-errors').hide();
        $('.train-success').show();
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        console.log(request);
        render.errorBlock(request);

        $('.cover').hide();
      }
    })
  }
}
