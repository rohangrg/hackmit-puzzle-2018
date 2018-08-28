This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

## Running
* `yarn install` to install dependencies
* `npm run watch-css` to watch Sass files
* `npm start` to run

Visit `{url}/:userhash` to try it out.

## Notes
* All state is stored in the `Game` component, and passed down to other
  components as props
* The only purpose of the `App` component is to pass the URL path into `Game`