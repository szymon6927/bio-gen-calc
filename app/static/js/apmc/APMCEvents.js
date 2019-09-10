"use strict";

const apmc = new APMCModule();
const preTrainForm = document.querySelector('#ml-pre-train-form');
const trainButton = document.querySelector('.train');

preTrainForm.addEventListener('submit', event => {
  event.preventDefault();
  apmc.preTrain();
});

trainButton.addEventListener('click', event => {
  event.preventDefault();
  apmc.train();
});
