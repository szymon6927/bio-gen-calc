function openMenu() {
  const overlay = $('#overlay');
  const sidebar = $('.sidebar');
  const hamburger = $('.hamburger')

  overlay.toggleClass('active');
  sidebar.toggleClass('active');
  hamburger.toggleClass('active');
}


$(document).ready(function() {
  $('.hamburger').click(function() {
    openMenu();  
  })
});