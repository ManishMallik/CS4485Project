import React, { useEffect, useState } from 'react';
import { tailChase } from 'ldrs'

tailChase.register("tail-chase")


const CompareResultsPopup = ({ results1, results2, onClose }) => {
  const [results, setResults] = useState([])
  useEffect(()=>{
    fetch(`http://127.0.0.1:5000/compare?id1=${results1}&id2=${results2}`)
    .then((response) => response.json())
    .then((data) => {
      setResults(data);
      console.log("RUN")
    })
  }, [])
  return (
    <div className="compare-results-popup">
      {
        results.length > 0?
        <div className="compare-results-container">
          <h2 style={{alignSelf: "flex-start"}}>Compare Results</h2>
          <div className="compare-results">
            <div>
              <h3>Result 1</h3>
                <div className='timeStamp'><p>Time: {results[0]["time"]}</p></div>
                <div><p>BENIGN: {results[0]["benign"]}</p></div>
                <div><p>DoS: {results[0]["dos"]}</p></div>
                <div><p>PortScan: {results[0]["portscan"]}</p></div>
                <div><p>Bot: {results[0]["bot"]}</p></div>
                <div><p>Infiltration: {results[0]["infiltration"]}</p></div>
                <div><p>WebAttack: {results[0]["webattack"]}</p></div>
                <div><p>BruteForce: {results[0]["bruteforce"]}</p></div>
            </div>
            <div>
              <h3>Result 2</h3>
                <div className='timeStamp'><p>Time: {results[1]["time"]}</p></div>
                <div><p>BENIGN: {results[1]["benign"]}</p></div>
                <div><p>DoS: {results[1]["dos"]}</p></div>
                <div><p>PortScan: {results[1]["portscan"]}</p></div>
                <div><p>Bot: {results[1]["bot"]}</p></div>
                <div><p>Infiltration: {results[1]["infiltration"]}</p></div>
                <div><p>WebAttack: {results[1]["webattack"]}</p></div>
                <div><p>BruteForce: {results[1]["bruteforce"]}</p></div>
            </div>
          </div>
          <button style={{margin: "auto", alignSelf: "center"}} onClick={onClose}>Close</button>
        </div>
        :
        <tail-chase color="white" size="40"></tail-chase>
      }
    </div>
  );
};

export default CompareResultsPopup;