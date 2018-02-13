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

function createMemory(next) {
	values = getValues()
	var data = JSON.stringify(values)
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
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
			url:'/timeline/api/add-memory',
			type: "POST",
			data: data,
			dataType: 'json',
      contentType: 'application/json; charset=utf-8',
			success:function(response){
				console.log(response)
			},
			complete:function(){},
			error:function (xhr, textStatus, thrownError){}
	});

}
