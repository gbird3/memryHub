// Use the API Loader script to load google.picker and gapi.auth.
function onGDriveButton() {
	document.getElementById("create-timeline").disabled = true;
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
    document.getElementById("create-timeline").disabled = false;
    document.getElementById("id_picture").value = docArray[0].id
    document.getElementById("id_title").value = docArray[0].name
  } else {
		document.getElementById("create-timeline").disabled = false;
	}
}
