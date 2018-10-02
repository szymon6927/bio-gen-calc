class DotPlot {

  buildJSONfromGeneBankSeq() {
    const firstID = $('#genebank-seq-1').val();
    const secondID = $('#genebank-seq-2').val();

    const data = {};
    data['seq-name-1'] = firstID;
    data['seq-name-2'] = secondID;

    return JSON.stringify(data);
  }

  buildJSONfromRawSeq() {
    const data = {};
    data['seq-name-1'] = $('#name-seq-1').val();
    data['seq-content-1'] = $('#content-seq-1').val();
    data['seq-name-2'] = $('#name-seq-2').val();
    data['seq-content-2'] = $('#content-seq-2').val();

    return JSON.stringify(data);
  }

  sendRawSeq() {
    $('.cover').show();
    const dataJSON = this.buildJSONfromRawSeq();
    console.log(dataJSON);
    const path = '/sequences-analysis-tools/dot-plot/send-raw-seq';
    const render = new RenderHelper('.dotplot-raw-seq-results');
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Succesfull", result);
        render.successBlock(result);

        const lastDivResult = $('.dotplot-raw-seq-results .result-score').last();

        const alignment = $(`<div class="row result-score alignment-wrapper">
                              <div class="title">Alignment:</div>
                              <pre class="alignment">${result.alignment}</pre>
                            </div>`);

        const dotPlotImg = $(`<div class="row result-score">
                                <img class="img-fluid dotplot-img" src="data:image/png;base64,${result.dotplot_base64}">
                              </div>`);

        dotPlotImg.insertAfter(lastDivResult);
        alignment.insertAfter(lastDivResult);

        $('.cover').hide();

        goToByScroll('.dotplot-raw-seq-results')
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);

        render.errorBlock(request);

        $('.cover').hide();
      }
    })
  }

  sendSeqGeneBank() {
    $('.cover').show();
    const dataJSON = this.buildJSONfromGeneBankSeq();
    const render = new RenderHelper('.genebank-seq-results');
    const path = '/sequences-analysis-tools/dot-plot/send-genebank-ids';

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      dataType: "json",
      success: function (result) {
        console.log("Succesfull", result);
        render.successBlock(result);

        const lastDivResult = $('.genebank-seq-results .result-score').last();

        const alignment = $(`<div class="row result-score alignment-wrapper">
                              <div class="title">Alignment:</div>
                              <pre class="alignment">${result.alignment}</pre>
                            </div>`);

        const dotPlotImg = $(`<div class="row result-score">
                                <img class="img-fluid dotplot-img" src="data:image/png;base64,${result.dotplot_base64}">
                              </div>`);

        dotPlotImg.insertAfter(lastDivResult);
        alignment.insertAfter(lastDivResult);

        $('.cover').hide();

        goToByScroll('.genebank-seq-results');
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);
        render.errorBlock(request);
        $('.cover').hide();
      }
    })
  }
}