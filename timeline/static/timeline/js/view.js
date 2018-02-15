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
