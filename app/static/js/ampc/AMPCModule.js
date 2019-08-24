"use strict";

class AMPCModule extends AppModule {
  constructor() {
    super();
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
}
