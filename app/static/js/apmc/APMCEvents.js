"use strict";

const ampc = new APMCModule();
const preTrainForm = document.querySelector('#ml-pre-train-form');
const trainButton = document.querySelector('.train');

preTrainForm.addEventListener('submit', event => {
  event.preventDefault();
  ampc.preTrain();
});

trainButton.addEventListener('click', event => {
  event.preventDefault();
  ampc.train();
});
