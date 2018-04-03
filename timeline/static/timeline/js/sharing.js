$( document ).ready(function() {
  $('[data-toggle="tooltip"]').tooltip()
});

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function share(num, timeline_id) {
  $('#share-success').hide();
  $('#share-email').hide();

  values = {
    email: document.getElementById(`new_user_email_${num}`).value,
    access: document.getElementById(`new_user_access_${num}`).value,
    timeline: timeline_id
  }

  if (values['email']) {
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
				url: "/timeline/api/share-timeline",
				type: "POST",
				data: values,
				success:function(response){
          if (response == 200) {
            $('#share-success').show();
            $(`#share_${num}`).html('Timeline Shared');
            document.getElementById(`share_${num}`).disabled = true;
          } else if (response == 201) {
            $('#share-email').show();
            $(`#share_${num}`).html('User invited');
            document.getElementById(`share_${num}`).disabled = true;
          } else {
            $('#share-fail').show();
          }
				},
				complete:function(){},
				error:function (xhr, textStatus, thrownError){}
    });
  } else {
    $('#new_user_email').css('border-color', 'red')
  }
}

function update(id) {
  values = {
    id: id,
    access: $('#' + id).val()
  }

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
      url: "/timeline/api/update-share-timeline",
      type: "POST",
      data: values,
      success:function(response){
        if (response == 200) {
          $('#share-success').show();
        } else {
          $('#share-fail').show();
        }
      },
      complete:function(){},
      error:function (xhr, textStatus, thrownError){}
  });


}
