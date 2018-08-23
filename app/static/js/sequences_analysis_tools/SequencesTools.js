class SequencesTools {

  buildJSON() {
    let type = $('#transformation-type').val();
    let seq = $('#fast-seq').val();

    let data = {};
    data['type'] = type;
    data['sequences'] = seq;

    return JSON.stringify(data);
  }

  sendData() {
    $('.cover').show();
    let dataJSON = this.buildJSON();
    const path = '/sequences-analysis-tools/sequences-tools/send-data';
    const render = new RenderHelper('.sequences-tools-results');
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Succesfull", result);

        render.successBlock(result);

        $('.cover').hide();
        goToByScroll('.sequences-tools-results');
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);

        $('.cover').hide();
        goToByScroll('.sequences-tools-results');
      }
    })
  }
}