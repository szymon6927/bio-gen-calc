"use strict";

const ampc = new AMPCModule();
const preTrainForm = document.querySelector('#ml-pre-train-form');

preTrainForm.addEventListener('submit', event => {
  event.preventDefault();
  ampc.preTrain();
});
