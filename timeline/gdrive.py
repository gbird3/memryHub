import requests
import json

url = 'https://www.googleapis.com/drive/v3/files'

def getHeaders(user):
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    return {
        'Authorization':'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

def sendRequest(url, headers, data):
    return requests.post(
        url,
        headers = headers,
        data = json.dumps(data)
    )

def createFolder(user, folderName, parents=None):

    headers = getHeaders(user)

    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parents:
        file_metadata['parents'] = [parents]

    response = sendRequest(url, headers, file_metadata)
    return response.json()

def changeFileName(user, fileId, file_name):
    file_metadata = {
        'title': file_name
    }

    updateUrl = '{}/{}'.format(url, fileId)

    response = sendRequest(updateUrl, getHeaders(user), file_metadata)

    return response
