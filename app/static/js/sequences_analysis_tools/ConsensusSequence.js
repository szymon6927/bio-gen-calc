class ConsensusSequence {

  buildJSONfromRawSeq() {
    let seq = $('#fast-seq').val();
    let data = {};
    data['sequences'] = seq;

    return JSON.stringify(data);
  }

  buildJSONfromGeneBankSeq() {
    let sequenceType = $('#type-of-sequence').val();
    let geneBankSeq = $('#gene-bank-seq').val();

    let data = {};
    data['sequence-type'] = sequenceType;
    data['genebank-seq'] = geneBankSeq;

    return JSON.stringify(data)
  }

  sendRawSeq() {
    $('.cover').show();
    const dataJSON = this.buildJSONfromRawSeq();
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

  sendSeqFile() {
    $('.cover').show();
    const render = new RenderHelper('.file-seq-results');
    const path = '/sequences-analysis-tools/consensus-sequence/send-seq-file';
    const file = new FormData($('#seq-upload-form')[0]);
    console.log(file);
    $.ajax({
      type: "POST",
      url: path,
      data: file,
      contentType: false,
      cache: false,
      processData: false,
      success: function (result) {
        console.log("Succesfull");

        $('.file-seq-results').html('<a id="download-link" download="consensus-sequence.fasta" style="display:none;"></a>');

        let downloadLink = document.getElementById('download-link');
        downloadLink.href = 'data:text/plain;base64,' + result;

        downloadLink.click();

        $('.cover').hide();
      },
      error: function (request) {
        console.log("Something goes wrong, try again!", request);
        render.errorBlock(request);
        $('.cover').hide();
      }
    });
  }

  sendSeqGeneBank() {
    $('.cover').show();
    const dataJSON = this.buildJSONfromGeneBankSeq();
    const render = new RenderHelper('.file-seq-genebank-results');
    const path = '/sequences-analysis-tools/consensus-sequence/send-genebank-file';

    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: path,
      data: dataJSON,
      cache: false,
      processData: false,
      success: function (result) {
        console.log("Succesfull");

        $('.file-seq-genebank-results').html('<a id="download-link" download="consensus-sequence.fasta" style="display:none;"></a>');

        let downloadLink = document.getElementById('download-link');
        downloadLink.href = 'data:text/plain;base64,' + result;

        downloadLink.click();

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