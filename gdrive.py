from __future__ import print_function
import pickle
import os.path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import argparse
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Use the application default credentials
cred = credentials.Certificate("danielkooeun/notepal-api/helpers/uofthacks-1547875157861-firebase-adminsdk-2gjh2-e584001b8e.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'uofthacks-1547875157861',
})

db = firestore.client()

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

    # Setup file metadata
    inputName = inputFile.split('/')[1].split('.')[0]
    metadata = {
        'name': inputName,
        'mimeType': 'application/pdf'
    }
    media = MediaFileUpload(inputFile,
                            mimetype='application/pdf',
                            resumable=True)
    file = service.files().create(body=metadata, media_body=media, fields='webViewLink, hasThumbnail, thumbnailLink').execute()
    print(file)

    doc_ref = db.collection(u'documents').document()
    doc_settings = {
        u'link': file['webViewLink'],
        u'name': unicode(inputName, 'utf-8')
    }

    if file['hasThumbnail']:
        doc_settings[u'thumbnail'] = file['thumbnailLink']
    doc_ref.set(doc_settings)
    print(file['webViewLink'])

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument("--filename", type=str, default="test")
   args = parser.parse_args()

   main(args.filename)
