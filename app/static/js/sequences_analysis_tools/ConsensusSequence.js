class ConsensusSequence {

  buildJSONfromRawSeq() {
    let seq = $('#fast-seq').val();
    let data = {};
    data['sequences'] = seq;

    return JSON.stringify(data);
  }

  sendRawSeq() {
    $('.cover').show();
    let dataJSON = this.buildJSONfromRawSeq();
    const path = '/sequences-analysis-tools/consensus-sequence/send-raw-seq';
    const render = new RenderHelper('.raw-seq-results');
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
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);

        $('.cover').hide();
      }
    })
  }
}