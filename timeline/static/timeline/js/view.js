$( document ).ready(function() {
  $('[data-toggle="tooltip"]').tooltip()
});

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

// A simple callback implementation.
function pickerCallback(data) {
  if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
    let docArray = data[google.picker.Response.DOCUMENTS]
    sendData(docArray).then(
      location.reload()
    )
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
