function renderSuccessMessage(msg) {
  const elem = $('.form-messages');
  const template = `<div class="alert alert-success text-center mt-2 mb-2" role="alert">
                      <span>${msg}</span>
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>`;
  elem.html(template);
}

function renderErrorMessage(msg) {
  const elem = $('.form-messages');
  const template = `<div class="alert alert-danger text-center mt-2 mb-2" role="alert">
                      <span>${msg}</span>
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>`;
  elem.html(template);
}

function addToNewsletter() {
  const path = '/newsletter/add';
  const email = $('#newsletter-email').val();
  const data = {
    'email': email
  };

  $.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: path,
    data: JSON.stringify(data),
    dataType: "json",
    success: (result) => {
      console.log("Successfull!", result);
      renderSuccessMessage(result.message);
    },
    error: (request) => {
      console.log("Something goes wrong, try again!", request);
      renderErrorMessage(request.responseText);
    }
  });

  $('.newsletter-form')[0].reset();
}


$('.newsletter-form').on('submit', (e) => {
  e.preventDefault();
  $('.alert').alert();
  addToNewsletter();
});