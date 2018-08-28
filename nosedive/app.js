const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const http = require('http');
const nunjucks = require('nunjucks');
const path = require('path');
const socketIO = require('socket.io');
const puppeteer = require('puppeteer');
const images = require('./media/images');
const rp = require('request-promise');
const Queue = require('promise-queue');

const app = express();
app.server = http.createServer(app);

nunjucks.configure(path.join(__dirname, 'views'), {
  autoescape: true,
  express: app,
	watch: true
});

// TODO: Add more images
// TODO: Make prime.html look pretty

/*
 * ENVIRONMENT VARIABLES
 * 
 * TIER = 
 * prod (production environment)
 * ~prod (anything else is development environment)
 * 
 */

// Get configuration of reCaptcha
const recaptchaConfig = require('./secrets/recaptcha')
const CAPTCHA_SERVER_SECRET_KEY = recaptchaConfig.SERVER_SECRET_KEY;
const CAPTCHA_SITE_KEY = recaptchaConfig.SITE_KEY;

/* PUZZLE SPECIFIC CONFIGURATIONS */
const DEFAULT_RATING = 3.7;
const BOOST_RATING = 5.0; // rating achievable only through hacking
const QUALIFYING_RATING = 4.4; // rating required in order to see the Prime Influencers Program boost button
const SOLUTION_RATING = 4.99; // need rating of 5.0 in order to win

const PUZZLE_SECRET = process.env.PUZZLE_SECRET || 'shhh';

const SUPPORT_DOMAIN = process.env.SUPPORT_DOMAIN || 'localhost';
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const DATABASE_URI = process.env.DATABASE_URI || 'sqlite://database.sqlite'

const ALLOWED_URL_PREFIXES = [
  `${BASE_URL}/u/`,
  `${BASE_URL}/beta/`,
  'https://cdnjs.cloudflare.com/',
];
const SUPPORT_TOKEN_SECRET = 'shhh';
const MAX_IMAGES = 38; // number of images in /media/images.js
const URL_REGEX = /https?:\/\/[A-Za-z0-9.\-_:]+[\/A-Za-z0-9.\-_]+/;
const UPDATE_BASE_DELAY = 6; // delay for when a user should get "rated back"
const UPDATE_RANDOM_DELAY = 10;

const DRAIN_PER_SEC = 3;
const MAX_CONCURRENT_TABS = 150;


const puzzleConfig = {
  DEFAULT_RATING,
  QUALIFYING_RATING,
  BOOST_RATING,
  SOLUTION_RATING,
  PUZZLE_SECRET,
  ALLOWED_URL_PREFIXES,
  SUPPORT_TOKEN_SECRET,
  SUPPORT_DOMAIN,
  MAX_IMAGES,
  URL_REGEX,
  UPDATE_BASE_DELAY,
  UPDATE_RANDOM_DELAY,
  CAPTCHA_SITE_KEY,
  DATABASE_URI
}
/* END PUZZLE SPECIFIC CONFIGURATIONS */

// Set up routers
const db = require('./models/user')(puzzleConfig);
const supportRouter = require('./routes/support')(puzzleConfig, db);
const usersRouter = require('./routes/users')(puzzleConfig, db);
const indexRouter = require('./routes/index');

const cannedResponses = {
  help: {
    regexPrototype: /help/,
    message: 'How can I help?'
  },
  hi: {
    regexPrototype: /( hello | hi |^hello |^hi |^hi$|^hello$)/,
    message: 'Hi there! How can I help?'
  },
  prime: {
    regexPrototype: /(prime|influencers|program|premium)/,
    message: `Hello! You can find out more about our Prime Influencers Programme <a href="${BASE_URL}/prime-influencers">here</a>.`
  },
  beta: {
    regexPrototype: /beta/,
    message: `Currently, only those who are admins, developers, and support have access to the Boost API.`
  }
}

let browser = null;
let io = socketIO(app.server);

let pageLoadQueue = new Queue(MAX_CONCURRENT_TABS, Infinity);

let loadPage = async (url, socket) => {
  //const ctx = await browser.createIncognitoBrowserContext();
  const page = await browser.newPage();

  await page.setCookie({
    name: 'support-token',
    value: puzzleConfig.SUPPORT_TOKEN_SECRET,
    domain: puzzleConfig.SUPPORT_DOMAIN,
    expires: (Date.now() / 1000) + 100000
  });

  await page.setRequestInterception(true);

  page.on('request', (interceptedRequest) => {
    let isAllowed = false;

    for (const allowedPrefix of puzzleConfig.ALLOWED_URL_PREFIXES) {
      if (interceptedRequest.url().startsWith(allowedPrefix)) {
        isAllowed = true;
        break;
      }
    }

    if (isAllowed)
      interceptedRequest.continue();
    else
      interceptedRequest.abort();
  });

  await page.goto(url);
  await page.waitFor(1000);
  await page.close();
  //await ctx.close();
  socket.emit('message', `Just finished checking out ${url}`);
  console.log(`[Q] ${pageLoadQueue.getPendingLength()-1} - ${pageLoadQueue.getQueueLength()} - ${url}`);
};

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

io.on('connection', (socket) => {
  let username = null;
  let bucket = 0.0;
  let last_t = undefined;

  socket.on('hello', (username_) => {
    username = username_;
    socket.emit('message', `Hi ${username}! If you need any help let me know. Customer support is always available.`);
    socket.emit('new-image', images[getRandomInt(MAX_IMAGES)], true);
  });

  socket.on('message', async (message) => {
    if(username == null)
      socket.disconnect();

    bucket += 1.0;
    let current_t = (new Date()).getTime();
    if (last_t !== undefined) {
      bucket = Math.max(bucket - (DRAIN_PER_SEC/1000)*(current_t - last_t), 0);
    }
    last_t = current_t;

    if (bucket > 2) {
      socket.emit('message', "You need to slow down sending messages. I'm disconnecting from you.");
      socket.disconnect();
      return;
    }

    let urlMatch = URL_REGEX.exec(message);
    if (urlMatch != null) {
      let isAllowed = false;

      for (const allowedPrefix of puzzleConfig.ALLOWED_URL_PREFIXES) {
        if (urlMatch[0].startsWith(allowedPrefix)) {
          isAllowed = true;
          break;
        }
      }

      if (isAllowed) {
        socket.emit('message', `Hm. Give me a second. I'll take a look at "${urlMatch}" right now.`);
        pageLoadQueue.add(() => loadPage(urlMatch[0], socket));
      } else {
        socket.emit('message', "Sorry I can't look at that link. It's not a \"safe\" work URL.");
      }
    } else {
      for (var resp in cannedResponses) {
        if (cannedResponses[resp].regexPrototype.test(message)) {
          socket.emit('message', cannedResponses[resp].message);
          return;
        }
      }
      socket.emit('message', `Sorry I don't understand what your problem is. Maybe if you gave me a link I could see.`);
    }
  });

  socket.on('rate', async (rating, captcha) => {
    // Do I need to check that rating, captcha are the right types?

    // Perform reCaptcha check
    let options = {
      method: 'POST',
      uri: 'https://www.google.com/recaptcha/api/siteverify',
      form: {
        secret: CAPTCHA_SERVER_SECRET_KEY,
        response: captcha
      }
    }

    let recaptchaCheck = await rp(options);
    recaptchaCheck = JSON.parse(recaptchaCheck);

    if (!recaptchaCheck.success) {
      return;
    }

    // Penalty if rating is artificially high
    if (rating > 5) {
      socket.emit('cheating-detected', "Cheating detected.", "We've detected illegal behavior from your account. We've applied a penalty as a cautionary measure.");
      rating = -rating;
      rating = Math.max(rating, -20);
    }

    // Send a new image
    socket.emit('new-image', images[getRandomInt(MAX_IMAGES)], false);

    // Update the user's rating at a random time after
    setTimeout(async (db) => {
      const userInfo = await db.getUserInfo(username);
      const newRating = Math.round(1000 * (0.99 * userInfo.rating + 0.01 * (Math.min(4.75, rating) - getRandomInt(2.5) / 10.0))) / 1000.0;

      await db.User.upsert({
        name: username,
        rating: newRating
      });

      socket.emit('rating-updated', "Rating updated!", "Someone just rated you back!", `${newRating}`)
    }, (UPDATE_BASE_DELAY + getRandomInt(UPDATE_RANDOM_DELAY)) * 1000, db);
  });
});

(async () => {
  if (process.env.TIER === 'prod') {
    console.log('[INFO] IN PRODUCTION ENVIRONMENT');
    browser = await puppeteer.launch();
  } else {
    console.log('[INFO] NOT IN A PRODUCTION ENVIRONMENT');
    browser = await puppeteer.launch({
      // TODO: Change this to an environment variable
      executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    });
  }
})();

app.use(express.static('public'));
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({
  extended: false
}));
app.use(cookieParser());

app.use('/', indexRouter);
app.use('/beta', supportRouter);
app.use('/u', usersRouter);

db.sequelize.sync().then(() => {
  app.server.listen(process.env.PORT || 3000, () => {
    console.log(`Started on port ${app.server.address().port}`);
  });
});

