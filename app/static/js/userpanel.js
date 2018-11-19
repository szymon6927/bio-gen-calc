function openMenu() {
  const overlay = $('#overlay');
  const sidebar = $('.sidebar');
  const hamburger = $('.hamburger')

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
  // $(`a[href="${url}"]`).addClass('active')
}


$(document).ready(function() {
  $('.hamburger').click(function() {
    openMenu();  
  })
  
  selectActiveMenuItem();
});