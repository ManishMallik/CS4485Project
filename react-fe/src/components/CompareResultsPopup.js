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
                <div><p>Model: {results[0]["model"]}</p></div>
                <div><p>Dataset: {results[0]["dataset"]}</p></div>
                <div><p>Accuracy: {results[0]["accuracy"]}</p></div>
                <div><p>F1-Score: {results[0]["f1score"]}</p></div>
                <div><p>Precision: {results[0]["precision"]}</p></div>
                <div><p>Recall: {results[0]["recall"]}</p></div>
                <div><p>F1 of DoS: {results[0]["dos"]}</p></div>
                <div><p>F1 of Sniffing: {results[0]["sniffing"]}</p></div>
                <div><p>F1 of Web Attack: {results[0]["webattack"]}</p></div>
                <div><p>F1 of Botnets: {results[0]["botnets"]}</p></div>
                <div><p>F1 of Infiltration: {results[0]["infiltration"]}</p></div>
                <div><p>Execution Time: {results[0]["time"]}</p></div>
            </div>
            <div>
              <h3>Result 2</h3>
                <div className='timeStamp'><p>Time: {results[1]["time"]}</p></div>
                <div><p>Model: {results[1]["model"]}</p></div>
                <div><p>Dataset: {results[1]["dataset"]}</p></div>
                <div><p>Accuracy: {results[1]["accuracy"]}</p></div>
                <div><p>F1-Score: {results[1]["f1score"]}</p></div>
                <div><p>Precision: {results[1]["precision"]}</p></div>
                <div><p>Recall: {results[1]["recall"]}</p></div>
                <div><p>F1 of DoS: {results[1]["dos"]}</p></div>
                <div><p>F1 of Sniffing: {results[1]["sniffing"]}</p></div>
                <div><p>F1 of Web Attack: {results[1]["webattack"]}</p></div>
                <div><p>F1 of Botnets: {results[1]["botnets"]}</p></div>
                <div><p>F1 of Infiltration: {results[0]["infiltration"]}</p></div>
                <div><p>Execution Time: {results[1]["time"]}</p></div>

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