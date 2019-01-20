from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import argparse
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main(inputFile):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'scripts/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)

    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    # print(items)

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

    # Setup file metadata
    metadata = {
        'name': inputFile,
        'mimeType': 'application/pdf'
    }
    media = MediaFileUpload(inputFile,
                            mimetype='application/pdf',
                            resumable=True)
    fileLink = (service.files().create(body=metadata, media_body=media, fields='webViewLink').execute())['webViewLink']
    print(fileLink)

    #results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name, webViewLink)").execute()
    #items = results.get('files', [])

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument("--filename", type=str, default="test")
   args = parser.parse_args()

   main(args.filename)