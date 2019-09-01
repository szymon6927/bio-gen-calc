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
      <div class="pre-train-result mb-3">
        <div class="item font-weight-bold">Model name: ${item.model_name}</div>
        <div class="item font-weight-bold">Accuracy: ${item.accuracy}</div>
        <div class="item font-weight-bold">Cross validate score: ${item.cross_validate_score}</div>
        <div class="table">${item.matrix_report}</div>
      </div>
      <hr>`
    });

    wrapper.html(template);
  }

  renderPreTrainResultsRegression(result) {
    const wrapper = $('.pre-train-results');
    let template = '';

    result.forEach((item, index) => {
      template += `
      <div class="pre-train-result mb-3">
        <div class="item font-weight-bold">Model name: ${item.model_name}</div>
        <div class="item font-weight-bold">Cross validate score: ${item.cross_validate_score}</div>
        <div class="item font-weight-bold">MAE: ${item.MAE}</div>
        <div class="item font-weight-bold">MSE: ${item.MSE}</div>
        <div class="item font-weight-bold">R2: ${item.R2}</div>
      </div>
      <hr>`
    });

    wrapper.html(template);
  }

  renderBestModelRecommendation(bestModelName) {
    const wrapper = $('.best-model-recommendation');

    const template = `
          <div class="card text-white bg-info mb-5 shadow-lg">
            <div class="card-header">
              <span class="info-icon"><i class="fas fa-info-circle"></i></span>
              <span class="card-title mb-0">Best model recommendation</span>
            </div>
            <div class="card-body">
              <p class="mb-0">For the best results we recommend to use:</p>
              <p><strong>${bestModelName}</strong></p>
            </div>
          </div>`;

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

        this.renderBestModelRecommendation(result.best_model);

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

  setPredictHref() {
    let predictButton = document.querySelector('.predict');
    predictButton.href = `/userpanel/models/${this.getAmpcDataID()}`
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
        this.setPredictHref();
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
