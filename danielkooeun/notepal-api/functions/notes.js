const ejs = require('ejs');
const moment = require('moment');
const firebase = require('../helpers/firebase-class');
const templatePath = __dirname + '/../templates/notes.ejs';

/**
* @returns {buffer}
*/

module.exports = (context, callback) => {
  const documents = firebase.collection('documents').get().then((documents) => {
    formatted = [];
    documents.forEach((doc) => {
      formatted.push({
        id: typeof doc.data().name === 'string'
          ? doc.data().name.replace(/\s+/g, '-').toLowerCase()
          : doc.id,
        name: doc.data().name,
        link: doc.data().link,
        thumbnail: doc.data().thumbnail,
        date: moment(doc._createTime._seconds*1000-21600000).format('lll'),
      });
    });
    return ejs.renderFile(
      templatePath,
      { documents: formatted },
      {},
      (err, response) => callback(err, Buffer.from(response || ''), {'Content-Type': 'text/html'})
    );
  });
};