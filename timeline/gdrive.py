import requests
import json

def createFolder(user, folderName, parents=None):
    url = 'https://www.googleapis.com/drive/v3/files'
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    headers = {
        'Authorization':'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parents:
        file_metadata['parents'] = [parents]

    response = requests.post(
        url,
        headers = headers,
        data = json.dumps(file_metadata)
    )

    return response.json()
