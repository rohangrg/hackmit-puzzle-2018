import React from 'react';
import styles from './Subcell.css';

const Subcell = (props) => {
  const subcellClassName = 'subcell' + props.dr + props.dc;
  let specialClass = null;
  if (props.dr === 1 && props.dc === 1) {
    if (props.dest) {
      specialClass = styles.house;
    } else if (props.here) {
      specialClass = styles.car;
    }
  }
  const rot = props.rot * 90 + 'deg';
  const style = {
    transform: `rotate(${rot})`
  }
  return (
    <div className={`${styles.container} ${styles[subcellClassName]}`}>
      <div className={`${styles[props.baseClass]}`} style={style}>

      </div>
      <div className={specialClass}>

      </div>
    </div>
  )
};

export default Subcell;