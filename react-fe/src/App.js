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


  const Tooltip = ({ text, metricName }) => (
    <span className="tooltip">
      <span className="tooltiptext">{text}</span>
      {metricName}:
    </span>
  );

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
        <h2>Choose a Dataset</h2>
        <div className="model-buttons">
          <button
            className={selectedData == 1 ? "selected" : " button"}
            onClick={() => handleDataSelect(1)}
          >CICIDS2017_sample.csv
          </button>
          <button
            className={selectedData === 2 ? "selected" : "button"}
            onClick={() => handleDataSelect(2)}
          >CICIDS2017_sample_km.csv
          </button>
        </div>
      </div>


      <div className="top-left section">
        <h2>Results</h2>
        <div className="results">
          <div>
            <Tooltip text="The accuracy metric measures the overall correctness of the model's predictions by comparing the number of correctly classified instances to the total number of instances." metricName="Accuracy" />
            <p>{round(result.accuracy)}</p>
          </div>
          <div>
            <Tooltip text="The F1-Score is a combined metric of precision and recall. For an IDS, a high F1-Score indicates a good balance between correctly identifying intrusions while minimizing false positives." metricName="F1-Score"/>
            <p>{round(result.f1score)}</p>
          </div>
          <div>
            <Tooltip text="Precision measures the accuracy of positive predictions made by the model. It signifies the proportion of correctly identified intrusions among all instances flagged as intrusions." metricName="Precision"/>
            <p>{round(result.precision)}</p>
            </div>
          <div>
            <Tooltip text="Recall measures the ability of the model to identify all positive instances correctly. Recall indicates the proportion of correctly identified intrusions among all actual intrusions. A high recall implies fewer false negatives, ensuring that most intrusions are detected." metricName="Recall"/>
            <p>{round(result.recall)}</p>
          </div>
          <div>
            <Tooltip text="The F1-Score of BENIGN assesses the model's ability to accurately classify normal network traffic while balancing false positives and false negatives." metricName="F1 of BENIGN"/>
            <p>{round(result.benign)}</p>
          </div>
          <div>
              <Tooltip text="The F1-Score of Bot indicates how effectively the model identifies botnet-related activities, such as command-and-control (C&C) communication or malware propagation, while considering both precision and recall." metricName="F1 of Bot"/>
              <p>{round(result.bot)}</p>
          </div>
          <div>
              <Tooltip text="This F1 score evaluates the model's capability to detect brute-force attacks, such as password guessing or credential stuffing, targeting web applications. It reflects the balance between accurately identifying brute-force attacks and minimizing false alarms." metricName="F1 of BruteForce"/>
              <p>{round(result.bruteforce)}</p>
          </div>
          <div>
              <Tooltip text="This F1-Score indicates how well the model detects Denial-of-Service (DoS) attacks, including flooding or resource depletion attempts, gauging the model's ability to distinguish DoS-related traffic from normal network behavior." metricName="F1 of DoS"/>
              <p>{round(result.dos)}</p>
          </div>
          <div>
              <Tooltip text="This F1-Score assesses the model's performance in identifying infiltration attempts, where attackers gain unauthorized access to a network or system. It represents the model's effectiveness in detecting intrusion attempts while minimizing both false positives and false negatives." metricName="F1 of Infiltration"/>
              <p>{round(result.infiltration)}</p>
          </div>
          <div>
              <Tooltip text="This F1-Score evaluates the model's ability to detect port scanning activities, where attackers search for open ports and services on a network, while balancing false positives and false negatives." metricName="F1 of PortScan"/>
              <p>{round(result.portscan)}</p>
          </div>
          <div>
              <Tooltip text="This F1-Score assesses the model's performance in identifying web-based attacks, such as SQL injection or cross-site scripting (XSS). It reflects the balance between accurately identifying web-based attacks and minimizing false alarms." metricName="F1 of WebAttack"/>
              <p>{round(result.webattack)}</p>
          </div>
          <div className="extime">
            <Tooltip text="This is the total time it took to run the chosen model and dataset." metricName="Execution Time"/>
            <p>{round(result.time)}</p>
          </div>
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