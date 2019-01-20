const fs = require('fs');
const fsp = require('fs').promises;
const readline = require('readline');
const {google} = require('googleapis');
const driveClass = require('./drive-class');

function main() {
  return driveClass;
}

module.exports = {
  uploadImage: main,
};