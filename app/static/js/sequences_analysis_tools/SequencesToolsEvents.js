"use strict";

const sequencesTools = new SequencesTools();

$('.sequences-tools-calculate').click(() => {
  sequencesTools.sendData();
});

$('.sequences-tools .save-calculation-form').submit(function(e) {
  e.preventDefault();
  sequencesTools.setContainer('.sequences-tools');
  sequencesTools.saveCalculation();
});
