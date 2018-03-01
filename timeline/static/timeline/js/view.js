function getValues() {
	let name = document.getElementById("memory_name").value;
	let year = document.getElementById("memory_year").value;
	let timeline = document.getElementById('timeline_id').value;

	return values = {
		name: name,
		year: year,
		timeline: timeline
	}
}

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function createMemory(next) {
	values = getValues()
	if (values['name'] && values['year']) {
		let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		values['next'] = next
		console.log(values)
		// set csrf header
		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});

		$.ajax({
				url: "/timeline/api/add-memory",
				type: "POST",
				data: values,
				// dataType: "json",
	      // contentType: "application/json; charset=utf-8",
				success:function(response){
					if (next === 'timeline') {
						location.reload()
					} else {
						location.replace(location.origin + '/timeline/memory/attach/' + response)
					}
				},
				complete:function(){},
				error:function (xhr, textStatus, thrownError){}
		});
	} else {
		document.getElementById('required-alert').removeAttribute('hidden')
	}

}





// Use the API Loader script to load google.picker and gapi.auth.
function onGDriveButton() {
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
			location.reload();
		})
  } else {
		document.getElementById("save-memory").disabled = false;
	}
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

      let name = doc.name;
      let id;

			$.ajax({
					url: "/timeline/api/attach-file",
					type: "POST",
					data: values,
					success:function(response) {},
					complete:function(){},
					error:function (xhr, textStatus, thrownError){}
			})
    }

		resolve(i)

	});
}
