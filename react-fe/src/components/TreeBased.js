import React, { useState } from 'react';
import './TreeBased.css'; // Import the CSS file

const Tooltip = ({ text }) => (
  <span className="tooltip">
    <span className="tooltiptext">{text}</span>
    ?
  </span>
);

const TreeBased = () => {
  const [parameters, setParameters] = useState({
    treebased_xgboost_learning_rate: '',
    treebased_xgboost_max_depth: '',
    treebased_xgboost_n_estimators: '',
    treebased_xgboost_colsample_bytree: '',
    treebased_xgboost_min_child_weight: '',

    treebased_rf_n_estimators: '',
    treebased_rf_max_depth: '',
    treebased_rf_min_samples_split: '',
    treebased_rf_min_samples_leaf: '',
    treebased_rf_max_features: '',
    treebased_rf_criterion: '',

    treebased_dt_max_depth: '',
    treebased_dt_min_samples_split: '',
    treebased_dt_min_samples_leaf: '',
    treebased_dt_max_features: '',
    treebased_dt_criterion: '',

    treebased_et_n_estimators: '',
    treebased_et_max_depth: '',
    treebased_et_min_samples_split: '',
    treebased_et_min_samples_leaf: '',
    treebased_et_max_features: '',
    treebased_et_criterion: '',

    treebased_classifier: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParameters(prevState => ({
      ...prevState,
      [name]: value
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
            name="treebased_xgboost_learning_rate"
            value={parameters.treebased_xgboost_learning_rate}
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
            name="treebased_xgboost_max_depth"
            value={parameters.treebased_xgboost_max_depth}
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
            name="treebased_xgboost_n_estimators"
            value={parameters.treebased_xgboost_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
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
      </div>
      <div className="parameter">
        <label>
        treebased_xgboost_min_child_weight
          <Tooltip text="This represents the minimum weight/requirement of evidence needed for a model to make a decision. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="treebased_xgboost_min_child_weight"
            value={parameters.treebased_xgboost_min_child_weight}
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
            name="treebased_rf_n_estimators"
            value={parameters.treebased_rf_n_estimators}
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
            name="treebased_rf_max_depth"
            value={parameters.treebased_rf_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
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
      </div>
      <div className="parameter">
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
      </div>
      <div className="parameter">
        <label>
        treebased_rf_max_features
          <Tooltip text="The number of features to consider when looking for the best split. (Input: a positive integer, a float where 0 < num <= 1, a string [options: ‘sqrt’ or ‘log2’, or None)" />
          :
          <input
            type="text"
            name="treebased_rf_max_features"
            value={parameters.treebased_rf_max_features}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
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
      </div>

      <div className="parameter">
  <label>
    treebased_dt_max_depth
    <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
    :
    <input
      type="number"
      name="treebased_dt_max_depth"
      value={parameters.treebased_dt_max_depth}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
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
</div>
<div className="parameter">
  <label>
    treebased_dt_min_samples_leaf
    <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting." />
    :
    <input
      type="number"
      name="treebased_dt_min_samples_leaf"
      value={parameters.treebased_dt_min_samples_leaf}
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
    <input
      type="text"
      name="treebased_dt_max_features"
      value={parameters.treebased_dt_max_features}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
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
</div>
<div className="parameter">
  <label>
    treebased_et_n_estimators
    <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
    :
    <input
      type="number"
      name="treebased_et_n_estimators"
      value={parameters.treebased_et_n_estimators}
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
      name="treebased_et_max_depth"
      value={parameters.treebased_et_max_depth}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
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
</div>
<div className="parameter">
  <label>
    treebased_et_min_samples_leaf
    <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting." />
    :
    <input
      type="number"
      name="treebased_et_min_samples_leaf"
      value={parameters.treebased_et_min_samples_leaf}
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
    <input
      type="text"
      name="treebased_et_max_features"
      value={parameters.treebased_et_max_features}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
<div className="parameter">
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
</div>
<div className="parameter">
  <label>
    treebased_classifier
    <Tooltip text="Choose between XGBoost, Random Forest, Decision Tree, Extra Tree, or ALL" />
    :
    <input
      type="text"
      name="treebased_classifier"
      value={parameters.treebased_classifier}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
    </div>
  );
};

export default TreeBased;