const fs = require('fs');
const fsp = require('fs').promises;
const readline = require('readline');
const {google} = require('googleapis');
const SCOPES = ['https://www.googleapis.com/auth/drive'];
const TOKEN_PATH = './helpers/token.json';

class Drive {
  constructor() {
    this.auth = authorize(JSON.parse(fs.readFileSync('./helpers/credentials.json')));
    this.drive = google.drive({version: 'v3', auth: this.auth});
  }
};

function authorize(credentials, callback=null) {
  const {client_secret, client_id, redirect_uris} = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0]);
  try {
    oAuth2Client.setCredentials(JSON.parse(fs.readFileSync(TOKEN_PATH)));
    return oAuth2Client;
  } catch (e) {
    if (e) return getAccessToken(oAuth2Client);
  }
}

function getAccessToken(oAuth2Client) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error('Error retrieving access token', err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
        if (err) console.error(err);
        console.log('Token stored to', TOKEN_PATH);
      });
      return oAuth2Client;
    });
  });
}

module.exports = new Drive();