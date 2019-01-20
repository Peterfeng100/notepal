import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("../uofthacks-1547875157861-firebase-adminsdk-2gjh2-e584001b8e.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'uofthacks-1547875157861',
})

db = firestore.client()

doc_ref = db.collection(u'documents').document(u'bobby')
doc_ref.set({
    u'link': u'https://drive.google.com/file/d/0B-axL5sab7OWMmctQXNNRUVLM0U',
    u'name': u'bobbybob'
})