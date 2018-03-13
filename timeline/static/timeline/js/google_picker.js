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
