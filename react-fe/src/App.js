import React, { useState, useEffect} from 'react';
import './App.css';
import DataTable from './components/DataTable.js';
import CompareResultsPopup from './components/CompareResultsPopup.js';
import LoadingButton from '@mui/lab/LoadingButton';
import LCCDE from './components/LCCDE.js';
import TreeBased from './components/TreeBased.js';
import MTH from './components/MTH.js';

import { bouncy } from 'ldrs'
bouncy.register('loading-bounce')

function App() {
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedData, setSelectedData] = useState(null);
  const [result, setResult] = useState({"benign":0,"bot":0,"bruteforce":0,"dataset":0,"dos":0,"id":0,"infiltration":0,"model":0,"portscan":0,"time":"NULL","webattack":0})
  const [presult, setPresult] = useState({})
  const [showLCCDE, setShowLCCDE] = useState(false);
  const [showTreeBased, setShowTreeBased] = useState(false);
  const [showMTH, setShowMTH] = useState(false);
  const [loaded, setLoaded] = useState(true)
  const [selected, setSelected] = useState([])
  

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
    if (model == 1) {
      setShowLCCDE(true)
      setSelectedData(1)
    }
    else {
      setShowLCCDE(false)
    }
    if (model == 2) {
      setShowTreeBased(true)
      setSelectedData(2)
    }
    else {
      setShowTreeBased(false)
    }
    if (model == 3) {
      setShowMTH(true)
      setSelectedData(2)
    }
    else {
      setShowMTH(false)
    }
    if (model == null) {
      setShowMTH(false)
      setShowTreeBased(false)
      setShowLCCDE(false)
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

  const handleCloseCompareResults = () => {
    setCompareResultsVisible(false);
    setSelected([])
  };

  const handlePastRun = () => {
    if (selected[0] != null && selected[1] == null)
      alert("yay button clicked successfully")
    else
      alert("broski u gotta select one")
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
          {/* /*<div className='timeStamp'><p>Time: {result.time}</p></div> */}
          <div><p>BruteForce: {result.bruteforce}</p></div>
          <div><p>Accuracy: 0</p></div>
          <div><p>F1-Score: 0</p></div>
          <div><p>Precision: 0</p></div>
          <div><p>Recall: 0</p></div>
        </div>
      </div>
      <div className="bottom-right section">
      <div>
        {selectedModel === 1 && showLCCDE && (
        <LCCDE />
      )}
        {selectedModel === 2 && showTreeBased && (
        <TreeBased />
      )}
        {selectedModel === 3 && showMTH && (
        <MTH />
      )}
  </div>
    {selectedModel !== null && (
      loaded ? 
        <button /*done loading*/ variant="outlined" className="runButton button" onClick={handleRunAlgorithm}>Run</button> :
        <button /*loading*/ variant="outlined" className="runButton button" >{<loading-bounce size="40"></loading-bounce>}</button>
    )}
      </div>
      <div className="bottom-left section">
        <div className="past-results-table">
          <DataTable setCompareResultsVisible={setCompareResultsVisible} selected={selected} setSelected={setSelected} passed_result={presult}></DataTable>
        </div>
        <div className="runs-button"> 
          <button className="past" onClick ={handlePastRun}>View Past Run</button> 
        </div>
      </div>

      {compareResultsVisible && (
        <CompareResultsPopup
          results1={selected[0]}
          results2={selected[1]}
          onClose={handleCloseCompareResults}
        />
      )}


    </div>
  );
}

export default App;