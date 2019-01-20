const admin = require('firebase-admin');
const serviceAccount = require('./uofthacks-1547875157861-firebase-adminsdk-2gjh2-e584001b8e.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
admin.firestore().settings({ timestampsInSnapshots: true });

module.exports = admin.firestore();