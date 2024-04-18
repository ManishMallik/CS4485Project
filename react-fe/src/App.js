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
  const [result, setResult] = useState({"accuracy": 0, "precision": 0, "recall": 0, "f1score": 0})
  const [presult, setPresult] = useState({})
  const [showLCCDE, setShowLCCDE] = useState(false);
  const [showTreeBased, setShowTreeBased] = useState(false);
  const [showMTH, setShowMTH] = useState(false);
  const [loaded, setLoaded] = useState(true)
  const [selected, setSelected] = useState([])
  
  const [data, setData] = useState({})

  const [compareResultsVisible, setCompareResultsVisible] = useState(false);
  const [comparedResult1, setComparedResult1] = useState({});
  const [comparedResult2, setComparedResult2] = useState({});

  function round(num){
    return Math.round((num + Number.EPSILON) * 1000000) / 1000000
  }

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
    let modelDict = {"model": selectedModel}
    let finalDict = {...modelDict, ...data}
    setLoaded(false)
    fetch('http://localhost:5000/runmodel?' + new URLSearchParams(finalDict))
    .then((response) => response.json())
    .then((data)=>{
      setResult(data)
      setLoaded(true)
      setSelectedModel(null);
      setSelectedData(null);
    })

  };

  const handleCloseCompareResults = () => {
    setCompareResultsVisible(false);
    setSelected([])
  };

  const handlePastRun = () => {
    if (selected[0] != null && selected[1] == null){
      fetch(`http://localhost:5000/pastrun?model=${selected[0]}`)
      .then((response) => response.json())
      .then((data) =>{
        // handleModelSelect(data[])
        console.log(data)
        setResult({"accuracy": data.accuracy, "precision": data.precision, "recall": data.recall, "f1score": data.f1score})
        handleModelSelect(data.model)
        setSelected([])
      })
    }
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
          <div><p>Accuracy: {round(result.accuracy)}</p></div>
          <div><p>F1-Score: {round(result.f1score)}</p></div>
          <div><p>Precision: {round(result.precision)}</p></div>
          <div><p>Recall: {round(result.recall)}</p></div>
        </div>
      </div>
      <div className="bottom-right section">
      <div>
        {selectedModel === 1 && showLCCDE && (
        <LCCDE setData={setData}/>
      )}
        {selectedModel === 2 && showTreeBased && (
        <TreeBased setData={setData}/>
      )}
        {selectedModel === 3 && showMTH && (
        <MTH setData={setData}/>
      )}
  </div>
    {selectedModel !== null && (
      loaded ? 
        <button /*done loading*/ variant="outlined" className="runButton button" onClick={handleRunAlgorithm}>Run</button> :
        <button /*loading*/ variant="outlined" className="runButton button disabled" >{<loading-bounce size="40"></loading-bounce>}</button>
    )}
      </div>
      <div className="bottom-left section">
        <div className="past-results-table">
          <DataTable setCompareResultsVisible={setCompareResultsVisible} selected={selected} setSelected={setSelected} passed_result={presult}></DataTable>
        </div>
        <div className="runs-button">
          {
            selected[0] != null ?
            <button className="past" onClick ={handlePastRun}>View Past Run</button> 
            :
            <button className="past disabled" disabled={true}>View Past Run</button> 


          }
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