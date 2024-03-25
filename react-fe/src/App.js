import React, { useState, useEffect} from 'react';
import './App.css';
import DataTable from './components/DataTable.js';

function App() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedData, setSelectedData] = useState(null);
  const [pastResults, setPastResults] = useState([]);

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
    setSelectedModel(null);
    setSelectedData(null);
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
            className={selectedModel === "Model1" ? "selected" : ""}
            onClick={() => handleModelSelect("Model1")}
          >LCCDE
          </button>
          <button 
            className={selectedModel === "Model2" ? "selected" : ""}
            onClick={() => handleModelSelect("Model2")}
          >Tree Based
          </button>
          <button 
            className={selectedModel === "Model3" ? "selected" : ""}
            onClick={() => handleModelSelect("Model3")}
          >MTH
          </button>
        </div>
      </div>
      <div className="top-left section">
        <h2>Results</h2>
        <div className="results">
          <div><p>TimeStamp: 0</p></div>
          <div><p>RunNumber: 0</p></div>
          <div><p>BENIGN: 0</p></div>
          <div><p>DoS: 0</p></div>
          <div><p>PortScan: 0</p></div>
          <div><p>Bot: 0</p></div>
          <div><p>Infiltration: 0</p></div>
          <div><p>WebAttack: 0</p></div>
          <div><p>BruteForce: 0</p></div>
        </div>
      </div>
      <div className="bottom-right section">
        <h2>Choose a Dataset</h2>
        <div className="data-section">
          <button 
          className={selectedData === "Data1" ? "selected" : ""}
          onClick={() => handleDataSelect("Data1")}
          >CICIDS2017_sample.csv
          </button>
          <button 
          className={selectedData === "Data2" ? "selected" : ""}
          onClick={() => handleDataSelect("Data2")}
          >CICIDS2017_sample_km.csv
          </button>
        </div>
        <button onClick={handleRunAlgorithm}>Run</button>
      </div>
      <div className="bottom-left section">
        <h2>Past Results</h2>
        {/* Display past results in a table */}
        <div className="past-results-table">
          <DataTable></DataTable>
        </div>
        <div className="action-buttons">
          <button onClick={handleCompareResults}>Compare</button>
        </div>
      </div>
    </div>
  );
}

export default App;