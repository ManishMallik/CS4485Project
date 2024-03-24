import React, { useState } from 'react';
import './App.css';
import DataTable from './components/DataTable.js';

function App() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [uploadedDataset, setUploadedDataset] = useState(null);
  const [pastResults, setPastResults] = useState([]);

  const handleModelSelect = (model) => {
    setSelectedModel(model);
  };

  const handleDatasetUpload = (e) => {
    const file = e.target.files[0];
    // Process the uploaded dataset file
    setUploadedDataset(file);
  };

  const handleRunAlgorithm = () => {
    // Implement logic to run the selected algorithm
    // and update pastResults state
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
          <button onClick={() => handleModelSelect("Model1")}>LCCDE</button>
          <button onClick={() => handleModelSelect("Model2")}>Tree Based</button>
          <button onClick={() => handleModelSelect("Model3")}>MTH</button>
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
        <h2>Upload Dataset</h2>
        <div className="data-section">
          <button onClick={() => handleModelSelect("Data1")}>Dataset 1</button>
          <button onClick={() => handleModelSelect("Data2")}>Dataset 2</button>
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
          <button onClick={handleViewResults}>View</button>
          <button onClick={handleRunAgain}>Run Again</button>
          <button onClick={handleCompareResults}>Compare</button>
        </div>
      </div>
    </div>
  );
}

export default App;