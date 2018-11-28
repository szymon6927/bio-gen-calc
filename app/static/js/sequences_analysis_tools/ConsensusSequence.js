"use strict";

class ConsensusSequence extends AppModule {
  constructor() {
    super();
  }

  buildJSONfromRawSeq() {
    let seq = $('#fast-seq').val();
    let threshold = $('#threshold-rawseq').val() || 0.55;
    let data = {};
    data['sequences'] = seq;
    data['threshold'] = parseFloat(threshold);

    return JSON.stringify(data);
  }

  buildJSONfromGeneBankSeq() {
    let sequenceType = $('#type-of-sequence').val();
    let geneBankSeq = $('#gene-bank-seq').val();
    let threshold = $('#threshold-genebank').val() || 0.55;

    let data = {};
    data['sequence-type'] = sequenceType;
    data['genebank-seq'] = geneBankSeq;
    data['threshold'] = parseFloat(threshold);

    return JSON.stringify(data)
  }

  async buildJSONfromFileSeq(fileInput, threshold) {

    try {
      const fileContents = await this.readFileContent(fileInput);
      let data = {};
      data['file-seq'] = fileContents;
      data['threshold'] = parseFloat(threshold);

      return JSON.stringify(data);
    }
    catch (e) {
      console.log(e.message);
    }
  }

  readFileContent(fileInput) {
    const file = fileInput.files[0];

    const temporaryFileReader = new FileReader();

    return new Promise((resolve, reject) => {

      temporaryFileReader.onerror = () => {
        temporaryFileReader.abort();
        reject(new DOMException("Problem parsing input file."));
      };

      temporaryFileReader.onload = () => {
        resolve(temporaryFileReader.result);
      };

      temporaryFileReader.readAsDataURL(file);
    });
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
      success: (result) => {
        console.log("Succesfull", result);

        render.successBlock(result);

        this.setResult(result);
        this.extendObjectToSave({'customer_input': dataJSON});

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

    let fileInput = document.getElementById('seq-file');
    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append('file', file);

    let threshold = $('#threshold-fileupload').val() || 0.55;
    formData.append('threshold', threshold);


    $.ajax({
      type: "POST",
      url: path,
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      success: (result) => {
        console.log("Succesfull");

        $('.file-seq-results').html('<a id="download-link" download="consensus-sequence.fasta" style="display:none;"></a>');

        let downloadLink = document.getElementById('download-link');
        downloadLink.href = 'data:text/plain;base64,' + result;

        downloadLink.click();

        this.buildJSONfromFileSeq(fileInput, threshold)
          .then((dataJSON) => {
            render.calculationBlock();
            this.setResult(result);
            this.extendObjectToSave({'customer_input': dataJSON});
            console.log(dataJSON);
          }).catch((req) => {
            console.log("Error: ", req);
        });

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
      success: (result) => {
        console.log("Succesfull");

        $('.file-seq-genebank-results').html('<a id="download-link" download="consensus-sequence.fasta" style="display:none;"></a>');

        let downloadLink = document.getElementById('download-link');
        downloadLink.href = 'data:text/plain;base64,' + result;

        console.log(result);

        downloadLink.click();

        render.calculationBlock();
        this.setResult(result);
        this.extendObjectToSave({'customer_input': dataJSON});

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