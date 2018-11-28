class AppModule {
  constructor() {
    this.result = {};
    this.userInput = {};
    this.container = '';
  }

  setResult(result) {
    this.result = result.data;
  }

  getResult() {
    return this.result;
  }

  setContainer(className) {
    this.container = className;
  }

  getContainer() {
    return this.container;
  }

  isEmpty(obj) {
    return Object.keys(obj).length === 0;
  }

  createObjectToSave() {
    const container = $(this.getContainer());
    const calculationForm = container.find('.save-calculation-form');

    this.userInput['customer_id'] = calculationForm.find('.customer-id').val();
    this.userInput['module_name'] = calculationForm.find('.module-name').val();
    this.userInput['title'] = calculationForm.find('.calculation-title').val();
    this.userInput['result'] = this.getResult();

    return this.userInput;
  }

  extendObjectToSave(addData) {
    if (!this.isEmpty(addData)) {
      Object.assign(this.userInput, addData);
    }
  }

  extendResultObject(data) {
    if (!this.isEmpty(data)) {
      this.result.push(data)
    }
  }

  clearInputAndHideMessage() {
    $(`${this.getContainer()} .save-calculation-form .calculation-title`).val("");
    $(`${this.getContainer()} .save-calculation-form .messages`).delay(5000).fadeOut('slow');
  }

  saveCalculation() {
    $('.cover').show();
    const render = new RenderHelper(`${this.getContainer()} .save-calculation-form .messages`);
    const calculation = this.createObjectToSave();

    const path = "/send-calculation";
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: JSON.stringify(calculation),
      dataType: "json",
      success: (result) => {
        console.log("Successfull!");
        render.successSaveCalculationBlock(result);
        $('.cover').hide();
        this.clearInputAndHideMessage();
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);
        render.errorBlock(request);
        $('.cover').hide();
      }
    })
  }
}