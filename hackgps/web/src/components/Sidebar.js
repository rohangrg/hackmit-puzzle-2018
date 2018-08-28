import React from 'react';
import styles from './Sidebar.css'

const Sidebar = (props) => (
  <div className={styles.container}>
    <div className={styles.inner}>
      <h1> HackGPS </h1>
      <p>
        The revolution of self-driving cars has come upon us - or has it?
        After years of AI research and no successful results, the engineers at HACK (Honestly Autonomous
        Car Kompany) realized that if autonomous cars were an impossibility, then
        "autonomous" cars are the next best thing.
      </p>
      <p>
        You have been hired as "autonomous" car driver ID: {props.userhash}. Tim wants to go back to his house (which is really far),
        and it's your job to navigate him there.
        The network connection from your console to his car is glitchy, and in this AI-forsaken dystopia, the roads seems
        poorly designed too...can you make it in time?
      </p>
      <br></br>
      { props.ready ?
        <div>
          <p>
            You have {props.timeRem} {props.timeRem === 1 ? 'minute' : 'minutes'} remaining.
            <button className={styles.button} onClick={props.handleReset}>Reset</button>
          </p>
          <br></br>
          <table>
            <tbody>
              <tr>
                <td></td>
                <td>
                  <button className={styles.movebutton} onClick={props.handleMove('up')}>&#8593;</button>
                </td>
                <td></td>
              </tr>
              <tr>
                <td>
                  <button className={styles.movebutton} onClick={props.handleMove('left')}>&#8592;</button>
                </td>
                <td></td>
                <td>
                  <button className={styles.movebutton} onClick={props.handleMove('right')}>&#8594;</button>
                </td>
              </tr>
              <tr>
                <td></td>
                <td>
                  <button className={styles.movebutton} onClick={props.handleMove('down')}>&#8595;</button>
                </td>
                <td></td>
              </tr>
            </tbody>
          </table>
          <small className={styles.footer}>Version {props.prob}</small>
        </div>
      : null }
    </div>
  </div>
)

export default Sidebar;