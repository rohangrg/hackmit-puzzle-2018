import React from 'react';
import Game from './Game';

const parsePath = (path) => {
  if (path.length < 4 || path.substring(0, 3) !== '/u/') {
    return '';
  }
  let newpath = path.substring(3);
  return newpath;
}

const App = () => {
  const hash = parsePath(window.location.pathname);
  if (hash.length > 0) {
    return <Game userhash={hash} />;
  } else {
    return <div> Bad path </div>;
  }
};

export default App;