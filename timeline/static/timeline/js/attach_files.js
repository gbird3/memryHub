// Use the API Loader script to load google.picker and gapi.auth.
function onGDriveButton() {
	document.getElementById("save-memory").disabled = true;
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
        addView(view).
        addView(new google.picker.DocsUploadView().setParent(parent_id)).
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

		sendData(docArray).then((fileCount) => {
			document.getElementById("save-memory").disabled = false;
			document.getElementById('file').innerHTML = ' Attached ' + fileCount + ' file(s).'
    	document.getElementById('file_div').removeAttribute('hidden')
		})
  } else {
		document.getElementById("save-memory").disabled = false;
	}
}

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendData(data) {
	return new Promise(function(resolve, reject) {
		let i = 0
		for (i; i < data.length; i++) {
      let doc = data[i]
			let type = doc.mimeType.indexOf('/')
			type = doc.mimeType.substring(0, type)

			let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

			let values = {
				type: type,
				name: doc.name,
				id: doc.id,
				memory_id: memory_id,
				description: doc.description
			}
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
					success:function(response){
					},
					complete:function(){},
					error:function (xhr, textStatus, thrownError){
					}
			})
    }

		resolve(i)

	});
}
