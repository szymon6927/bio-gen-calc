"use strict";

const hw = new HardyWeinber();

$('.calculate-hw').click(function () {
  let ho = $('#ho').val();
  let he = $('#he').val();
  let rho = $('#rho').val();
  let alfa = $('#alfa').val();

  if (!hw.validateData(ho, he, rho)) {
    showModal('Please insert int values');
    return false;
  }

  if ((ho == 0 && he == 0) || (he == 0 && rho == 0)) {
    showModal('Incorrect validation, more than two values are equal to 0 !');
    return false;
  }


  hw.setHo(ho);
  hw.setHe(he);
  hw.setRho(rho);
  hw.setAlpha(alfa);


  hw.sendData();

  setTimeout(() => {
    goToByScroll('.hw-results');
  }, 300)
});

$('.form-control').keypress(function (e) {
  if (e.which == 13) {
    $('.calculate-hw').trigger('click');
    return false;
  }
});

$('.hardy-weinberg .save-calculation-form').submit(function(e) {
  e.preventDefault();
  hw.setContainer('.hardy-weinberg');
  hw.saveCalculation();
});
