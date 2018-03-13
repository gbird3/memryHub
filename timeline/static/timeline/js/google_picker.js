// Use the API Loader script to load google.picker and gapi.auth.
// The Browser API key obtained from the Google API Console.
const developerKey = 'AIzaSyByL9-SR6OjZfHaV-YIQlxmFn9SeGTxKO8';

// The Client ID obtained from the Google API Console. Replace with your own Client ID.
const clientId = "416104053530-7lar744p4o8b7jqstahqiuovabi6qd4a.apps.googleusercontent.com"
let pickerApiLoaded = false;

function onGDriveButton(memory_id, parent_id) {
  window.memory_id = memory_id
  window.parent_id = parent_id
  gapi.load('picker', {'callback': onPickerApiLoad});
}

function onPickerApiLoad() {
  pickerApiLoaded = true;
  createPicker();
}

function createPicker() {
  if (pickerApiLoaded && oauthToken) {
    let view = new google.picker.View(google.picker.ViewId.DOCS);
    var picker = new google.picker.PickerBuilder().
        enableFeature(google.picker.Feature.MULTISELECT_ENABLED).
        addView(new google.picker.DocsUploadView().setParent(window.parent_id)).
        addView(view).
        setOAuthToken(oauthToken).
        setDeveloperKey(developerKey).
        setCallback(pickerCallback).
        build();
    picker.setVisible(true);
  }
}

// A simple callback implementation.
function pickerCallback(data) {
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    let docArray = data[google.picker.Response.DOCUMENTS]
    sendData(docArray).then(
      location.reload()
    )
  }
}

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendData(data) {
	return new Promise(function(resolve, reject) {
		let i = 0
    let info = [];

		for (i; i < data.length; i++) {
      let doc = data[i]
			let type = doc.mimeType.indexOf('/')
			type = doc.mimeType.substring(0, type)

			let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

			let values = {
				type: type,
				name: doc.name,
				id: doc.id,
				memory_id: window.memory_id,
				description: doc.description
			}

      sendApiRequest(values, csrftoken)
    }
    resolve(i)
	});
}


function sendApiRequest(values, csrftoken) {
  return new Promise(function(resolve, reject) {
    // set csrf header
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        url: "/timeline/api/attach-file",
        type: "POST",
        data: values,
        success:function(response) {},
        complete:function(){},
        error:function (xhr, textStatus, thrownError){}
    })

    resolve()
  });
}
