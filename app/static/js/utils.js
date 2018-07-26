class Validation {

  keyAllowed(key) {
    var keys = [8, 9, 13, 16, 17, 18, 19, 20, 27, 46, 48, 49, 50,
      51, 52, 53, 54, 55, 56, 57, 91, 92, 93
    ];
    if (key && keys.indexOf(key) === -1)
      return false;
    else
      return true;
  }

  nonNegative(selector='.non-negative') {
    let self = this;
    let inputs = document.querySelectorAll(selector);
    inputs.forEach(function (element) {

      element.addEventListener('keypress', function (e) {
        var key = !isNaN(e.charCode) ? e.charCode : e.keyCode;
        if (!self.keyAllowed(key))
          e.preventDefault();
      }, false);

      // Disable pasting of non-numbers
      element.addEventListener('paste', function (e) {
        var pasteData = e.clipboardData.getData('text/plain');
        if (pasteData.match(/[^0-9]/))
          e.preventDefault();
      }, false);
    })
  }

  floatBetween01(selector='.float01') {
    let valid = true;
    let inputs = document.querySelectorAll(selector);


    $(selector).removeClass('is-invalid');
    $('.invalid-feedback').hide();

    inputs.forEach(function(element) {
      let patern =  /^(0(\.[0-9]+)?|1(.0)?)$/;
      let value = element.value;
      if (!patern.test(value)) {
        valid = false;
        $(element).addClass('is-invalid');
        $(element).next().show();
      }
    });

    return valid
  }

}

function showModal(message) {
  let modal = $('#message-modal')
  modal.modal('show')
  modal.find('.modal-body p').html(message)
}

$('#message-modal').modal({
  show: false
})

$(document).ready(function () {
  const validator = new Validation()
  validator.nonNegative('.non-negative')
  // validateNegative()
})
