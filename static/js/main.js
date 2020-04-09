$(document).ready(function(){
    let ckeditor;
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    let maxArticleLength = 15000;

    // Set and show ckeditor instance. Save instance in variable.
    ClassicEditor
      .create( document.querySelector( '#editor' ), {
        toolbar: [
          'heading',
          '|',
          'bold',
          'italic',
          'link',
          'bulletedList',
          'numberedList',
          '|',
          'indent',
          'outdent',
          '|',
          'codeBlock',
          'imageUpload',
          'blockQuote',
          'insertTable',
          'mediaEmbed',
          'undo',
          'redo'
        ],
        image: {
          toolbar: [
            'imageTextAlternative',
            'imageStyle:full',
            'imageStyle:side'
          ],
          upload: {
            types: [ 'jpeg', 'png', 'gif', 'webp', 'tiff' ]
          }
        },
        simpleUpload: {
            uploadUrl: 'http://127.0.0.1:8000/upload/',
            headers: {
              'X-CSRFToken': csrf_token,
            }
        }
      } )
      .then( editor => {
          ckeditor = editor;
      } )
      .catch( error => {
          console.error( error );
      } );

    getArticleLength = function() {
      data = ckeditor.getData();
      return data.length;
    };

    $('#editor-submit').click(function() {
      httpRequest = new XMLHttpRequest();

      if (!httpRequest) {
        alert('Failed create http request!');
        return false;
      }

      // Setting url for uploads
      let url = 'upload/';

      // Receive response and print it
      // Function is called, when response is received
      httpRequest.onload = function() {
        let response = httpRequest.response;
        
        console.log(response.title);
        console.log(response.body);
        console.log(response.world);
      };

      let articleLength = getArticleLength();
      if (articleLength <= maxArticleLength) {

        // Setting and sending ajax request
        httpRequest.open('POST', url, true);
        httpRequest.setRequestHeader('X-Content-Type-Options', 'nosniff');
        httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        httpRequest.setRequestHeader('X-CSRFToken', csrf_token);
        httpRequest.responseType = "json";
        httpRequest.send('article_body=' + encodeURIComponent(ckeditor.getData()));
      } else {
        alert(
              'Article is too long. Maximum allowed length is ' + maxArticleLength +
              ' characters. Your article has ' + articleLength + ' symbols.'
             );
      };
    } )
});