import requests
import json
from social_django.utils import load_strategy

def getAccessToken(user):
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']
    return social.get_access_token(load_strategy())

def getHeaders(user):
    access_token = getAccessToken(user)

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

def sendUpdateRequest(url, headers, data):
    return requests.put(
        url,
        params = {'uploadType': 'multipart', 'alt': 'json'},
        headers = headers,
        data = json.dumps(data)
    )

def patchRequest(url, headers, data):
    return requests.patch(
        url,
        headers = headers,
        data = json.dumps(data)
    )

def createFolder(user, folderName, parents=None):
    url = 'https://www.googleapis.com/drive/v3/files'
    headers = getHeaders(user)

    file_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parents:
        file_metadata['parents'] = [parents]

    response = sendRequest(url, headers, file_metadata)
    return response.json()

def changeFileData(user, fileId, file_name, description):
    url = 'https://www.googleapis.com/drive/v2/files'
    file_metadata = {
        'title': file_name,
        'description': description
    }

    updateUrl = '{}/{}'.format(url, fileId)

    response = sendUpdateRequest(updateUrl, getHeaders(user), file_metadata)

    return response

def shareWithUser(owner, userEmail, fileId, role):
    url = 'https://www.googleapis.com/drive/v3/files/{}/permissions'.format(fileId)

    body = {
        'role': role,
        'type': 'user',
        'emailAddress': userEmail
    }

    return sendRequest(url, getHeaders(owner), body)

def updateSharing(owner, permissionId, fileId, role):
    url = 'https://www.googleapis.com/drive/v2/files/{}/permissions/{}'.format(fileId, permissionId)

    body = {
        'role': role,
    }

    return patchRequest(url, getHeaders(owner), body)
