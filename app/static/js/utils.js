function keyAllowed(key) {
  var keys = [8, 9, 13, 16, 17, 18, 19, 20, 27, 46, 48, 49, 50,
    51, 52, 53, 54, 55, 56, 57, 91, 92, 93
  ];
  if (key && keys.indexOf(key) === -1)
    return false;
  else
    return true;
}

function validateNegative() {
  var inputs = document.querySelectorAll(".non-negative");

  inputs.forEach(function (element) {

    element.addEventListener('keypress', function (e) {
      var key = !isNaN(e.charCode) ? e.charCode : e.keyCode;
      if (!keyAllowed(key))
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

function showModal(message) {
  let modal = $('#message-modal')
  modal.modal('show')
  modal.find('.modal-body p').html(message)
}

$('#message-modal').modal({
  show: false
})

$(document).ready(function () {
  validateNegative()
})
