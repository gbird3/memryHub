function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function createTimeline(next) {
	values = {
    name: document.getElementById("timeline_name").value
  }

	if (values['name']) {
		let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		// set csrf header
		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});

		$.ajax({
				url: "/timeline/api/add-timeline",
				type: "POST",
				data: values,
				// dataType: "json",
	      // contentType: "application/json; charset=utf-8",
				success:function(response){
					if (next === 'timeline') {
						//location.reload()
						location.replace(location.origin + '/timeline/view/' + response)
					} else {
						location.replace(location.origin + '/timeline/edit/' + response)
					}
				},
				complete:function(){},
				error:function (xhr, textStatus, thrownError){}
		});
	} else {
		document.getElementById('required-alert').removeAttribute('hidden')
	}

}
