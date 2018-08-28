const crypto = require('crypto'),
      fs = require('fs');

const WORDS = fs.readFileSync(__dirname + '/words.txt', 'utf8').trim().split('\n').map((x) => x.trim().toLowerCase());

function comhash(secret, username) {
  const hash = crypto.createHash('sha256');
  hash.update(username.toLowerCase().trim() + secret, 'utf8');
  const digest = hash.digest();
  const out = [];
  for(let i = 0; i < 3; i++) {
    out.push(WORDS[digest.readUInt32LE(i*4) % WORDS.length]);
  }
  return out.join(' ');
}

module.exports = comhash;
