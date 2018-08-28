module.exports = function (config, userModel) {
  const express = require('express');
  const router = express.Router();
  const {
    _,
    User,
    getUserInfo
  } = userModel;

  let puzzleConfig = config;

  router.get('/api', async (req, res) => {
    res.render('api.html');
  });

  router.get('/signup', async (req, res) => {
    res.render('signup.html');
  });

  router.post('/signup', async (req, res) => {
    let username = req.body.username;
    let userInfo = await getUserInfo(username);

    if (userInfo.rating >= puzzleConfig.QUALIFYING_RATING) {
      res.render('thanks.html');
    } else {
      res.render('sorry.html');
    }
  });

  /*router.use(function authenticate(req, res, next) {
    if (req.cookies['support-token'] == puzzleConfig.SUPPORT_TOKEN_SECRET) {
      next();
    } else {
      res.send("get outta here you aren't support");
    }
  });*/

  router.post('/boost_rating', async (req, res) => {
    if (req.cookies['support-token'] == puzzleConfig.SUPPORT_TOKEN_SECRET) {
      console.log("VALID TOKEN");
      const username = req.body.username;
      await User.upsert({
        name: username,
        rating: puzzleConfig.BOOST_RATING
      });
      res.send("done");
    } else {
      res.status(401).send("get outta here you aren't support");

    }
  });

  return router;
}
