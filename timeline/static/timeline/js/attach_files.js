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

jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});
