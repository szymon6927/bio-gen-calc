function darkModeSwitcher() {
  const toggler = document.querySelector('#switch');

  if (toggler.checked) {
    addDarkTheme();
  }
  else {
    removeDarkTheme();
  }

}

function checkOnLoad() {
  const toggler = document.querySelector('#switch');

  if (isDarkMode()) {
    toggler.checked = true;
    addDarkTheme();
  }

}

function addDarkTheme() {
  const darkCSS = '<link id="dark-theme" rel="stylesheet" href="/static/css/dark-style.css">';

  let tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  let expiresDate = tomorrow.toUTCString();

  document.cookie = `darkmode=on; expires=${expiresDate}`;
  $('head').append(darkCSS);
}

function removeDarkTheme() {
  $('#dark-theme').remove();
  document.cookie = `darkmode=off;`;
}

function isDarkMode() {
  return document.cookie.match(/darkmode=on/i) || undefined;
}

$(document).ready(function() {
  checkOnLoad();
});

$('#switch').click(function() {
  darkModeSwitcher();
});