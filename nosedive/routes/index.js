const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.send('go back to command center kiddo');
});

router.get('/prime-influencers', (req, res) => {
  res.render('prime.html');
});


module.exports = router;