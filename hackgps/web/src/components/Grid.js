import React, { Component } from 'react';
import Cell from './Cell';
import styles from './Grid.css';
import { isValid, toNode } from '../utils';

class Grid extends Component {
  getRoadType(r1, c1, r2, c2) {
    /*
    returns 0 if no road exists between (r1, c1) and (r2, c2)
    returns 1 if only outbound road exists from (r1, c1) to (r2, c2)
    returns 2 if inbound road exists from (r2, c2) to (r1, c1)
    */
    if (
      !isValid(r1, c1, this.props.gridH, this.props.gridW) ||
      !isValid(r2, c2, this.props.gridH, this.props.gridW)
    ) {
          return 0;
    }
    const v1 = toNode(r1, c1, this.props.gridH, this.props.gridW);
    const v2 = toNode(r2, c2, this.props.gridH, this.props.gridW);
    if (this.props.adjList[v2].indexOf(v1) > -1) {
      return 2;
    } else if (this.props.adjList[v1].indexOf(v2) > -1) {
      return 1;
    } else {
      return 0;
    }
  }

  getRoadTypes(r, c) {
    const output = {
      N: this.getRoadType(r, c, r - 1, c),
      E: this.getRoadType(r, c, r, c + 1),
      S: this.getRoadType(r, c, r + 1, c),
      W: this.getRoadType(r, c, r, c - 1)
    }
    return output;
  }

  render() {
    // only render the cells within range of the current cell
    if (this.props.ready) {
      const range = 2;
      let coords = [];
      for (let r = this.props.curRow - range; r <= this.props.curRow + range; r++) {
        for (let c = this.props.curCol - range; c <= this.props.curCol + range; c++) {
          if (r >= 0 && r < this.props.gridH && c >= 0 && c < this.props.gridW) {
            coords.push([r, c]);
          }
        }
      }
      const neighCells = coords.map((coord) =>
        <Cell key={coord[0].toString() + '-' + coord[1].toString()}
          drow={coord[0] - this.props.curRow} dcol={coord[1] - this.props.curCol}
          roadTypes={this.getRoadTypes(coord[0], coord[1])}
          dest={coord[0] === this.props.gridH - 1 && coord[1] === this.props.gridW - 1}/>
      );
      return (
        <div className={styles.container}>
          {neighCells}
        </div>
      );
    } else {
      return (
        <div className={styles.container}>Map loading...</div>
      );
    }
  }
}

export default Grid;