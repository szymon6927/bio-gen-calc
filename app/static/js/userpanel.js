function openMenu() {
  const overlay = $('#overlay');
  const sidebar = $('.sidebar');
  const hamburger = $('.hamburger');

  overlay.toggleClass('active');
  sidebar.toggleClass('active');
  hamburger.toggleClass('active');
}

function selectActiveMenuItem() {
  const url = window.location.pathname;
  $('.nav-item a').removeClass('active');
  let activeItem = $(`a[href="${url}"]`);

  activeItem.addClass('active');

  if (activeItem.hasClass('dropdown-item')) {
    let parent = activeItem.parents('.nav-item.dropdown');
    parent.addClass('active');
  }
}

function positionFooter() {
  let footerHeight = 0,
    footerTop = 0,
    $footer = $(".footer");

  footerHeight = $footer.height();
  // 20 is as padding height
  footerTop = ($(window).scrollTop() + $(window).height() - footerHeight - 80) + "px";

  if (($(document.body).height() + footerHeight) < $(window).height()) {
    $footer.css({
      position: "absolute",
      width: "100%"
    }).animate({
      top: footerTop
    })
  }
  else {
    $footer.css({
      position: "relative"
    })
  }

}

function showInputFileName() {
  let file = $('#picture')[0].files[0]
  if (file) {
    $('.custom-file label').text(file.name);
  }
}

function initCKEDITOR(selector) {
  ClassicEditor
      .create(document.querySelector(`${selector}`))
      .then(editor => {
        theEditor = editor;
      })
      .catch(error => {
        console.error(error);
      });
}

function confirmPageDelete() {
  return confirm("Are you sure to delete this?");
}

function goToByScroll(className) {
  if (!className.includes('.')) {
    className = "." + className
  }

  $('html, body').animate({
    scrollTop: $(className).offset().top - 80
  }, 1200);
}

function showLoader() {
  const loaderWrapper = $('.cover');
  loaderWrapper.show();
}


$(document).ready(function() {
  const deleteActionClassList = '.delete-page, .delete-customer, .delete-apmc-data, .delete-calculation,' +
    ' .delete-package, .delete-mail, .delete-article, .delete-feed';

  $('.hamburger').click(function() {
    openMenu();
  });

  selectActiveMenuItem();

  $('#picture').change(function() {
    showInputFileName();
  });

  $(deleteActionClassList).click(function (e) {
    if (!confirmPageDelete()) {
      e.preventDefault();
    }
  });

  $('.run-scrapper').click(function () {
    showLoader();
  })
});

$(window).bind("load", function () {
  positionFooter();
});

$(window)
  .scroll(positionFooter)
  .resize(positionFooter);
