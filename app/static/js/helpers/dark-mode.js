function darkModeSwitcher() {
  const darkCSS = '<link id="dark-theme" rel="stylesheet" href="/static/css/dark-style.css">';

  let tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  let expiresDate = tomorrow.toUTCString();

  if (isDarkMode() === undefined) {
    document.cookie = `darkmode=on; expires=${expiresDate}`;
    $('head').append(darkCSS);
  }
  else {
    $('#dark-theme').remove();
    document.cookie = `darkmode=off; expires=${expiresDate}`;
  }
}

function isDarkMode() {
  return document.cookie.match(/darkmode=on/i) || undefined
}


$(document).ready(function() {  
  $('#switch').click(function() {
    darkModeSwitcher();
  })
});