import React, { useState, useEffect} from 'react';
import './App.css';
import DataTable from './components/DataTable.js';
import CompareResultsPopup from './components/CompareResultsPopup.js';
import LoadingButton from '@mui/lab/LoadingButton';

import { bouncy } from 'ldrs'
bouncy.register('loading-bounce')

function App() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedData, setSelectedData] = useState(null);
  const [result, setResult] = useState({"benign":0,"bot":0,"bruteforce":0,"dataset":0,"dos":0,"id":0,"infiltration":0,"model":0,"portscan":0,"time":"NULL","webattack":0})
  const [presult, setPresult] = useState({})
  const [loaded, setLoaded] = useState(true)

  const [compareResultsVisible, setCompareResultsVisible] = useState(false);
  const [comparedResult1, setComparedResult1] = useState({});
  const [comparedResult2, setComparedResult2] = useState({});

  useEffect(()=>{
    setPresult(result)
  }, [result])
  useEffect(()=>{
    console.log(loaded)
  }, [loaded])



  const handleModelSelect = (model) => {
    setSelectedModel(model);
    if (selectedModel == model) {
      setSelectedModel(null);
    }
  };

  const handleDataSelect = (data) => {
    setSelectedData(data);
    if (selectedData == data) {
      setSelectedData(null);
    }
  };

  const handleButtonClick = (buttonType, value) => {
    if (buttonType === 'model') {
      setSelectedModel(value);
    } else if (buttonType === 'data') {
      setSelectedData(value);
    }
  };

  const handleRunAlgorithm = (m, d) => {
    // Implement logic to run the selected algorithm
    // and update pastResults state
    if(selectedModel != null && selectedData != null){
      setLoaded(false)
      fetch(`http://localhost:5000/sendinfo?model_type=${selectedModel}&dataset=${selectedData}`)
      .then((response)=>response.json())
      .then((data) =>{
        setResult(data)
        setLoaded(true)
      })
      setSelectedModel(null);
      setSelectedData(null);
    }
  };

  const handleViewResults = () => {
    // Implement logic to view the results of the current run
  };

  const handleRunAgain = () => {
    // Implement logic to run the algorithm again using the same dataset and model
  };

  
  const handleCompareResults = () => {
    // Implement logic to compare past results
    // For demonstration, let's compare the current result with an empty result
    setComparedResult1(result);
    setComparedResult2({});
    setCompareResultsVisible(true);
  };

  const handleCloseCompareResults = () => {
    setCompareResultsVisible(false);
  };



  return (
    <div className="App">
      <div className="top-right section">
        <h2>Choose a Model</h2>
        <div className="model-buttons">
          <button
            className={selectedModel == 1 ? "selected" : " button"}
            onClick={() => handleModelSelect(1)}
          >LCCDE
          </button>
          <button
            className={selectedModel === 2 ? "selected" : "button"}
            onClick={() => handleModelSelect(2)}
          >Tree Based
          </button>
          <button
            className={selectedModel === 3 ? "selected" : " button"}
            onClick={() => handleModelSelect(3)}
          >MTH
          </button>
        </div>
      </div>
      <div className="top-left section">
        <h2>Results</h2>
        <div className="results">
          <div><p>BENIGN: {result.benign}</p></div>
          <div><p>DoS: {result.dos}</p></div>
          <div><p>PortScan: {result.portscan}</p></div>
          <div><p>Bot: {result.bot}</p></div>
          <div><p>Infiltration: {result.infiltration}</p></div>
          <div><p>WebAttack: {result.webattack}</p></div>
          <div className='timeStamp'><p>Time: {result.time}</p></div>
          <div><p>BruteForce: {result.bruteforce}</p></div>
        </div>
      </div>
      <div className="bottom-right section">
        <h2>Choose a Dataset</h2>
        <div className="data-section">
          <button 
          className={selectedData == 1 ? "selected" : "button"}
          onClick={() => {handleDataSelect(1)}}
          >CICIDS2017_sample.csv
          </button>
          <button 
          className={selectedData == 2 ? "selected" : "button"}
          onClick={() => handleDataSelect(2)}
          >CICIDS2017_sample_km.csv
          </button>
        </div>
        {
          loaded ? 
          <button /*done loading*/ variant="outlined" className="runButton button" onClick={handleRunAlgorithm}>Run</button> :
          <button /*loading*/ variant="outlined" className="runButton button" >{<loading-bounce size="40"></loading-bounce>}</button>

        }
      </div>
      <div className="bottom-left section">
        <h2>Past Results</h2>
        {/* Display past results in a table */}
        <div className="past-results-table">
          <DataTable passed_result={presult}></DataTable>
        </div>
        <div className="action-buttons">
          <button className="button" onClick={handleCompareResults}>Compare</button>
        </div>
      </div>

      {compareResultsVisible && (
        <CompareResultsPopup
          results1={comparedResult1}
          results2={comparedResult2}
          onClose={handleCloseCompareResults}
        />
      )}

    </div>
  );
}

export default App;