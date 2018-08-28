module.exports = function (config) {
  let puzzleConfig = config;

  const Sequelize = require('sequelize');

  const sequelize = new Sequelize(config.DATABASE_URI, {
    operatorsAliases: false,
    logging: false
  });

  const User = sequelize.define('user', {
    name: {
      type: Sequelize.STRING,
      unique: true
    },
    rating: {
      type: Sequelize.FLOAT,
      defaultValue: puzzleConfig.DEFAULT_RATING
    },
    bio: Sequelize.STRING
  });

  let getUserInfo = async (username) => {
    const user = await User.findOne({
      where: {
        name: `${username}`
      }
    });

    let userInfo = {
      bio: "",
      rating: puzzleConfig.DEFAULT_RATING
    };

    if (user !== null) {
      userInfo.rating = user.rating;
      userInfo.bio = user.bio;
    }

    return userInfo;
  };

  const userModel = {
    sequelize,
    User,
    getUserInfo
  };

  return userModel;
}
