import React, { useEffect, useState } from 'react';
import './TreeBased.css'; // Import the CSS file

const Tooltip = ({ text }) => (
  <span className="tooltip">
    <span className="tooltiptext">{text}</span>
    ?
  </span>
);

const TreeBased = (props) => {
  const [parameters, setParameters] = useState({
    xgb_lr: '0.1',
    xgb_depth: '3',
    xgb_n_est: '100',
    xgb_min_weight: '1',
    
    rf_n_est: '100',
    rf_depth: 'None',
    rf_features: 'sqrt',
    
    dt_depth: 'None',
    dt_leaf: '1',
    dt_features: 'None',
    
    et_n_est: '100',
    et_depth: 'None',
    et_leaf: '1',
    et_features: 'sqrt',
    
    classifier: 'all',
  });
  useEffect(()=>{
    props.setData(parameters)
  }, [parameters])
  const handleChange = (e) => {
    const { name, value } = e.target;

    // Input validation for positive integers
    if (
      name.includes('_n_est') ||
      name.includes('depth') ||
      name.includes('leaf') ||
      name.includes('_min_weight')
    ) {
      if (!/^\d+$/.test(value)) {
        // Not a positive integer, show error
        alert('Please enter a positive integer.');
        return;
      }
    }

    // Input validation for values between 0 and 1
    if (name === 'treebased_xgboost_colsample_bytree') {
      const floatValue = parseFloat(value);
      if (isNaN(floatValue) || floatValue < 0 || floatValue > 1) {
        // Not a valid value, show error
        alert('Please enter a number between 0 and 1.');
        return;
      }
    }

    setParameters((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleDropdownChange = (e) => {
    const { name, value } = e.target;
    setParameters((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  return (
    <div className="treebased-container">
      <div className="parameter">
        <label>
        treebased_xgboost_learning_rate 
          <Tooltip text="It controls how quickly the model learns from the given data. A higher learning rate will have the model learn faster but can sacrifice accuracy, while a lower learning rate will have the model learn slower but more accurately. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="xgb_lr"
            value={parameters.xgb_lr}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
        treebased_xgboost_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="xgb_depth"
            value={parameters.xgb_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
        treebased_xgboost_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="xgb_n_est"
            value={parameters.xgb_n_est}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
        treebased_xgboost_colsample_bytree
          <Tooltip text="This determines the variety of decision-making features the model considers at each round. More variety can help prevent the model from focusing too much on one type of feature. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="treebased_xgboost_colsample_bytree"
            value={parameters.treebased_xgboost_colsample_bytree}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
        treebased_xgboost_min_child_weight
          <Tooltip text="This represents the minimum weight/requirement of evidence needed for a model to make a decision. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="xgb_min_weight"
            value={parameters.xgb_min_weight}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
        treebased_rf_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="rf_n_est"
            value={parameters.rf_n_est}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
        treebased_rf_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="rf_depth"
            value={parameters.rf_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
        treebased_rf_min_samples_split
          <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting. (Input: A nonnegative integer)" />
          :
          <input
            type="number"
            name="treebased_rf_min_samples_split"
            value={parameters.treebased_rf_min_samples_split}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      {/* <div className="parameter">
        <label>
        treebased_rf_min_samples_leaf
          <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="treebased_rf_min_samples_leaf"
            value={parameters.treebased_rf_min_samples_leaf}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
        treebased_rf_max_features
          <Tooltip text="The number of features to consider when looking for the best split. (Input: a positive integer, a float where 0 < num <= 1, a string [options: ‘sqrt’ or ‘log2’, or None)" />
          :
          <select
        name="rf_features"
        value={parameters.rf_features}
        onChange={handleChange}
        className="parameter-input"
      >
        <option value="sqrt">sqrt</option>
        <option value="log2">log2</option>
        <option value="None">None</option>
      </select>
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          treebased_rf_criterion
          <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
          :
          <input
            type="text"
            name="treebased_rf_criterion"
            value={parameters.treebased_rf_criterion}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}

      <div className="parameter">
  <label>
    treebased_dt_max_depth
    <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
    :
    <input
      type="number"
      name="dt_depth"
      value={parameters.dt_depth}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
{/* <div className="parameter">
  <label>
    treebased_dt_min_samples_split
    <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting." />
    :
    <input
      type="number"
      name="treebased_dt_min_samples_split"
      value={parameters.treebased_dt_min_samples_split}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div> */}
<div className="parameter">
  <label>
    treebased_dt_min_samples_leaf
    <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting." />
    :
    <input
      type="number"
      name="dt_leaf"
      value={parameters.dt_leaf}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
  <label>
    treebased_dt_max_features
    <Tooltip text="The number of features to consider when looking for the best split." />
    :
    <select
        name="dt_features"
        value={parameters.dt_features}
        onChange={handleChange}
        className="parameter-input"
      >
        <option value="sqrt">sqrt</option>
        <option value="log2">log2</option>
        <option value="None">None</option>
      </select>
  </label>
</div>
{/* <div className="parameter">
  <label>
    treebased_dt_criterion
    <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
    :
    <input
      type="text"
      name="treebased_dt_criterion"
      value={parameters.treebased_dt_criterion}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div> */}
<div className="parameter">
  <label>
    treebased_et_n_estimators
    <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
    :
    <input
      type="number"
      name="et_n_est"
      value={parameters.et_n_est}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
  <label>
    treebased_et_max_depth
    <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
    :
    <input
      type="number"
      name="et_depth"
      value={parameters.et_depth}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
{/* <div className="parameter">
  <label>
    treebased_et_min_samples_split
    <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting." />
    :
    <input
      type="number"
      name="treebased_et_min_samples_split"
      value={parameters.treebased_et_min_samples_split}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div> */}
<div className="parameter">
  <label>
    treebased_et_min_samples_leaf
    <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting." />
    :
    <input
      type="number"
      name="et_leaf"
      value={parameters.et_leaf}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
  <label>
    treebased_et_max_features
    <Tooltip text="The number of features to consider when looking for the best split." />
    :
    <select
        name="et_features"
        value={parameters.et_features}
        onChange={handleChange}
        className="parameter-input"
      >
        <option value="sqrt">sqrt</option>
        <option value="log2">log2</option>
        <option value="None">None</option>
      </select>
  </label>
</div>
{/* <div className="parameter">
  <label>
    treebased_et_criterion
    <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
    :
    <input
      type="text"
      name="treebased_et_criterion"
      value={parameters.treebased_et_criterion}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div> */}
<div className="parameter">
  <label>
    treebased_classifier
    <Tooltip text="Choose between XGBoost, Random Forest, Decision Tree, Extra Tree, or ALL" />
    :
    <select
    name="classifier"
    value={parameters.classifier}
    onChange={handleDropdownChange}
    className="parameter-input"
  >
            <option value="all">all</option>
            <option value="xgboost">xgboost</option>
            <option value="random forest">random forest</option>
            <option value="decision tree">decision tree</option>
            <option value="extra tree">decision tree</option>
  </select>
  </label>
</div>
    </div>
  );
};

export default TreeBased;