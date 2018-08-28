const comhash = require('../../comhash/comhash.js');

module.exports = function (config, userModel) {

  const express = require('express');
  const router = express.Router();
  const {
    _,
    User,
    getUserInfo
  } = userModel;
  const emoji = require('node-emoji');

  let puzzleConfig = null;

  let getSolution = (username, rating) => {
    if (rating >= puzzleConfig.SOLUTION_RATING) {
      return comhash(config.PUZZLE_SECRET, username);
    } else {
      return null;
    }
  };

  let getStatus = (rating) => {
    if (rating < 3.0) {
      return '<img src="/imgs/yuck.png" alt="Yuck" width="24px"></img>';
    } else if (rating < 3.5) {
      return '<img src="/imgs/no.png" alt="No" width="24px"></img>';
    } else if (rating < 4.0) {
      return '<img src="/imgs/thumbs-down.png" alt="Thumbs Down" width="24px"></img>';
    } else if (rating < 4.4) {
      return '<img src="/imgs/thinking.png" alt="Thinking" width="24px"></img>';
    } else if (rating < 4.6) {
      return '<img src="/imgs/fire.png" alt="Fire" width="24px"></img>';
    } else if (rating < 4.8) {
      return '<img src="/imgs/100.png" alt="100" width="24px"></img>';
    } else if (rating < 5.0) {
      return '<img src="/imgs/star-struck.png" alt="Star Struck" width="24px"></img>';
    } else {
      return '<img src="/imgs/crown.png" alt="Crown" width="24px"></img>';
    }
  };

  router.get('/:username', async (req, res) => {
    const username = req.params.username;
    const userInfo = await getUserInfo(username);
    const solution = getSolution(username, userInfo.rating);
    const bioError = 'bio_error' in req.query;

    res.render('index.html', {
      username: username,
      rating: userInfo.rating,
      bio: userInfo.bio,
      bioError: bioError,
      solution: solution,
      qualifying: userInfo.rating >= puzzleConfig.QUALIFYING_RATING,
      qualifying_rating: puzzleConfig.QUALIFYING_RATING,
      solution_rating: puzzleConfig.SOLUTION_RATING,
      status: getStatus(userInfo.rating),
      key: puzzleConfig.CAPTCHA_SITE_KEY
    });
  });

  router.post('/:username', async (req, res) => {
    const bio = req.body.bio || "";
    const username = req.params.username;

    if (bio.length > 255) {
      res.redirect(`/u/${username}?bio_error`);
      return;
    }

    // TODO use postgres upsert return values
    await User.upsert({
      name: username,
      bio: bio
    });

    res.redirect(`/u/${username}`);
  });

  router.post('/:username/boost_rating', async (req, res) => {
    res.send('Sorry, this feature is still in beta.');
  })

  puzzleConfig = config;
  return router;
}
