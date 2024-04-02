import React from 'react';

const CompareResultsPopup = ({ results1, results2, onClose }) => {
  return (
    <div className="compare-results-popup">
      <div className="compare-results-container">
        <h2>Compare Results</h2>
        <div className="compare-results">
          <div>
            <h3>Results 1</h3>
              <div className='timeStamp'><p>Time: 0</p></div>
              <div><p>BENIGN: 0</p></div>
              <div><p>DoS: 0</p></div>
              <div><p>PortScan: 0</p></div>
              <div><p>Bot: 0</p></div>
              <div><p>Infiltration: 0</p></div>
              <div><p>WebAttack: 0</p></div>
              <div><p>BruteForce: 0</p></div>
          </div>
          <div>
            <h3>Results 2</h3>
              <div className='timeStamp'><p>Time: 0</p></div>
              <div><p>BENIGN: 0</p></div>
              <div><p>DoS: 0</p></div>
              <div><p>PortScan: 0</p></div>
              <div><p>Bot: 0</p></div>
              <div><p>Infiltration: 0</p></div>
              <div><p>WebAttack: 0</p></div>
              <div><p>BruteForce: 0</p></div>
          </div>
        </div>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default CompareResultsPopup;