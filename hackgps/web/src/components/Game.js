import React, { Component } from 'react';
import Sidebar from './Sidebar';
import Grid from './Grid';
// import { isValid, toNode } from '../utils';

class Game extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userhash: '',
      adjList: [],
      gridH: 0,
      gridW: 0,
      timeRem: 0,
      curRow: 0,
      curCol: 0,
      prob: 0,
      ready: false,
    };
    this.handleMove = this.handleMove.bind(this);
    this.handleReset = this.handleReset.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.poll = this.poll.bind(this);
  }

  updateState(firstTime) {
    const endpoints = ['map', 'position', 'time', 'probability'];
    const promises = endpoints.map(endpoint => fetch('/api/' + endpoint + '?user=' + this.props.userhash));
    Promise.all(promises)
    .then(results => {
      return Promise.all(results.map(result => result.json()));
    })
    .then(jsonResults => {
      let states = [];
      for (let i = 0; i < jsonResults.length; i++) {
        if (endpoints[i] === 'map') {
          const adjList = jsonResults[i]['graph'];
          states.push(this.setState({
            adjList: adjList,
            gridH: Math.sqrt(adjList.length),
            gridW: Math.sqrt(adjList.length),
          }));
        } else if (endpoints[i] === 'position') {
          states.push(this.setState({
            curRow: jsonResults[i]['row'],
            curCol: jsonResults[i]['col'],
          }));
        } else if (endpoints[i] === 'time') {
          states.push(this.setState({
            timeRem: jsonResults[i]['time'],
          }));
        } else if (endpoints[i] === 'probability') {
          states.push(this.setState({
            prob: jsonResults[i]['probability'],
          }));
        }
      }
      return Promise.all(states);
    })
    .then(res => {
      return this.setState({
        ready: true
      });
    })
    .then(res => {
      if (firstTime) {
        this.poll();
      }
    });
  }

  handleReset() {
    this.setState({
      ready: false
    });
    fetch('/api/reset?user=' + this.props.userhash, {method: 'POST'})
    .then(res => {
      this.updateState(false);
    })
  }

  handleMove(dir) {
    return () => {
      if (this.state.ready) {
        fetch('/api/move?user=' + this.state.userhash +'&move=' + dir, {method: 'POST'})
        .then(result => {
          return result.json();
        })
        .then(jsonResult => {
          if ('message' in jsonResult && !('time' in jsonResult)) {
            alert(jsonResult['message']);
          }
          if ('row' in jsonResult && 'col' in jsonResult) {
            this.setState({
              curRow : jsonResult['row'],
              curCol : jsonResult['col']
            });
          }
          if ('time' in jsonResult) {
            this.setState({
              timeRem : jsonResult['time']
            })
          }
        });
      }
    };
  }

  handleKeyPress(e) {
    const keyMap = {
      37: 'left',
      38: 'up',
      39: 'right',
      40: 'down'
    }
    if (e.keyCode in keyMap) {
      this.handleMove(keyMap[e.keyCode])();
    }
  }

  poll() {
    if (this.state && this.state.ready) {
      Promise.all(
        [
          fetch('/api/position?user=' + this.state.userhash),
          fetch('/api/time?user=' + this.state.userhash)
        ]
      ).then(results => {
        try {
          return Promise.all(results.map(result => result.json()));
        } catch(err) {
          return Promise.resolve([]);
        }
      })
      .then(resJson => {
        if (resJson.length > 0) {
          if ('row' in resJson[0] && 'col' in resJson[0] && 'time' in resJson[1]) {
            return this.setState({
              curRow : resJson[0]['row'],
              curCol : resJson[0]['col'],
              timeRem : resJson[1]['time']
            });
          }
        }
        return Promise.resolve();
      })
      .then(() => {
        setTimeout(this.poll, 2000);
      });
    } else {
      setTimeout(this.poll, 2000);
    }
  }

  componentDidMount() {
    this.setState({
      userhash : this.props.userhash,
      ready : false
    });
    this.updateState(true);
  }

  render() {
    return (
      <div onKeyDown={this.handleKeyPress} tabIndex="0">
        <Sidebar userhash={this.state.userhash} timeLim={this.state.timeLim}
          timeRem={this.state.timeRem} prob={this.state.prob} handleMove={this.handleMove}
          handleReset={this.handleReset} ready={this.state.ready}/>
        <Grid userhash={this.state.userhash} adjList={this.state.adjList}
          gridW={this.state.gridW} gridH={this.state.gridH}
          curRow={this.state.curRow} curCol={this.state.curCol} ready={this.state.ready}/>
      </div>
    )
  }
}

export default Game;