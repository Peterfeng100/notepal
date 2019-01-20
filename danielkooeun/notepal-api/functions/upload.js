const { uploadImage } = require('../helpers/drive');

/**
* @returns {string}
*/

module.exports = async (context) => {
  const res = await uploadImage().drive.files.create({
    requestBody: {
      name: 'bob.png',
      mimeType: 'image/png',
    },
    media: {
      mimeType: 'image/png',
      body: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Small-city-symbol.svg/893px-Small-city-symbol.svg.png',
    },
  });
  console.log(res.data);
  return res.data.toString();
};