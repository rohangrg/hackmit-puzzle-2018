import React from 'react';
import Subcell from './Subcell';
import styles from './Cell.css';

const Cell = (props) => {

  let subcells = [];
  for (let dr = 0; dr < 3; dr++) {
    for (let dc = 0; dc < 3; dc++) {
      let roadClass = '0000';
      if (dr === 0 && dc === 1 && props.roadTypes['N'] > 0) {
        roadClass = `${props.roadTypes['N']}010`;
      }
      if (dr === 2 && dc === 1 && props.roadTypes['S'] > 0) {
        roadClass = `10${props.roadTypes['S']}0`;
      }
      if (dr === 1 && dc === 0 && props.roadTypes['W'] > 0) {
        roadClass = `010${props.roadTypes['W']}`;
      }
      if (dr === 1 && dc === 2 && props.roadTypes['E'] > 0) {
        roadClass = `0${props.roadTypes['E']}01`;
      }

      if (dr === 1 && dc === 1) {
        roadClass = '';
        for (let dir in props.roadTypes) {
          roadClass += props.roadTypes[dir] > 0 ? '1' : '0';
        }
      }
      // rotations
      let rot = 0;
      let baseClass = roadClass;

      const getScore = (str) => {
        let score = 0;
        let pow = 8;
        for (let i = 0; i < 4; i++) {
          score += parseInt(str[i]) * pow;
          pow /= 2;
        }
        return score;
      }

      let maxScore = getScore(roadClass, 0);

      for (let newrot = 1; newrot < 4; newrot++) {
        let newClass = '';
        for (let i = 0; i < 4; i++) {
          newClass += roadClass[(i + newrot) % 4];
        }
        if (getScore(newClass) > maxScore) {
          maxScore = getScore(newClass);
          rot = newrot;
          baseClass = newClass;
        }
      }

      baseClass = 'r' + baseClass;

      subcells.push(
        <Subcell key={dr+'-'+dc} dr={dr} dc={dc}
          here={props.drow === 0 && props.dcol === 0}
          dest={props.dest} baseClass={baseClass} rot={rot}/>
      )
    }
  }

  const cellClassName = 'cell' + props.drow + props.dcol;
  return (
    <div className={`${styles.container} ${styles[cellClassName]}`} >
      {subcells}
    </div>
  );

}

export default Cell;