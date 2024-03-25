import React, { useState, useEffect} from 'react';
import './App.css';
import DataTable from './components/DataTable.js';

function App() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedData, setSelectedData] = useState(null);
  const [result, setResult] = useState({"benign":0,"bot":0,"bruteforce":0,"dataset":0,"dos":0,"id":0,"infiltration":0,"model":0,"portscan":0,"time":"NULL","webattack":0})
  const [presult, setPresult] = useState({})
  useEffect(()=>{
    setPresult(result)
  }, [result])

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
      fetch(`http://localhost:5000/sendinfo?model_type=${selectedModel}&dataset=${selectedData}`)
      .then((response)=>response.json())
      .then((data) =>{
        setResult(data)
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
        <button className="runButton button" onClick={handleRunAlgorithm}>Run</button>
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
    </div>
  );
}

export default App;