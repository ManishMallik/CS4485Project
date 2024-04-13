import React, { useState } from 'react';
import './MTH.css'; // Import the CSS file

const Tooltip = ({ text }) => (
  <span className="tooltip">
    <span className="tooltiptext">{text}</span>
    ?
  </span>
);

const MTH = () => {
  const [parameters, setParameters] = useState({
    mth_xgboost_learning_rate: '',
    mth_xgboost_max_depth: '',
    mth_xgboost_n_estimators: '',
    mth_xgboost_colsample_bytree: '',
    mth_xgboost_min_child_weight: '',

    mth_rf_n_estimators: '',
    mth_rf_max_depth: '',
    mth_rf_min_samples_split: '',
    mth_rf_min_samples_leaf: '',
    mth_rf_max_features: '',
    mth_rf_criterion: '',

    mth_dt_max_depth: '',
    mth_dt_min_samples_split: '',
    mth_dt_min_samples_leaf: '',
    mth_dt_max_features: '',
    mth_dt_criterion: '',

    mth_et_n_estimators: '',
    mth_et_max_depth: '',
    mth_et_min_samples_split: '',
    mth_et_min_samples_leaf: '',
    mth_et_max_features: '',
    mth_et_criterion: '',

    mth_classifier: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParameters(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  return (
    <div className="mth-container">
      <div className="parameter">
        <label>
          mth_xgboost_learning_rate
          <Tooltip text="It controls how quickly the model learns from the given data. A higher learning rate will have the model learn faster but can sacrifice accuracy, while a lower learning rate will have the model learn slower but more accurately. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="mth_xgboost_learning_rate"
            value={parameters.mth_xgboost_learning_rate}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_xgboost_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_xgboost_max_depth"
            value={parameters.mth_xgboost_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_xgboost_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_xgboost_n_estimators"
            value={parameters.mth_xgboost_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_xgboost_colsample_bytree
          <Tooltip text="This determines the variety of decision-making features the model considers at each round. More variety can help prevent the model from focusing too much on one type of feature. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="mth_xgboost_colsample_bytree"
            value={parameters.mth_xgboost_colsample_bytree}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_xgboost_min_child_weight
          <Tooltip text="This represents the minimum weight/requirement of evidence needed for a model to make a decision. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="mth_xgboost_min_child_weight"
            value={parameters.mth_xgboost_min_child_weight}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_rf_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_rf_n_estimators"
            value={parameters.mth_rf_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_rf_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_rf_max_depth"
            value={parameters.mth_rf_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_rf_min_samples_split
          <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting. (Input: A nonnegative integer)" />
          :
          <input
            type="number"
            name="mth_rf_min_samples_split"
            value={parameters.mth_rf_min_samples_split}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      {/* <div className="parameter">
        <label>
          mth_rf_min_samples_leaf
          <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_rf_min_samples_leaf"
            value={parameters.mth_rf_min_samples_leaf}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_rf_max_features
          <Tooltip text="The number of features to consider when looking for the best split. (Input: a positive integer)" />
          :
          <input
            type="number"
            name="mth_rf_max_features"
            value={parameters.mth_rf_max_features}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_rf_criterion
          <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
          :
          <input
            type="text"
            name="mth_rf_criterion"
            value={parameters.mth_rf_criterion}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_dt_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_dt_max_depth"
            value={parameters.mth_dt_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_dt_min_samples_split
          <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting. (Input: A nonnegative integer)" />
          :
          <input
            type="number"
            name="mth_dt_min_samples_split"
            value={parameters.mth_dt_min_samples_split}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_dt_min_samples_leaf
          <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_dt_min_samples_leaf"
            value={parameters.mth_dt_min_samples_leaf}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_dt_max_features
          <Tooltip text="The number of features to consider when looking for the best split. (Input: a positive integer)" />
          :
          <input
            type="number"
            name="mth_dt_max_features"
            value={parameters.mth_dt_max_features}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_dt_criterion
          <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
          :
          <input
            type="text"
            name="mth_dt_criterion"
            value={parameters.mth_dt_criterion}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_et_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_et_n_estimators"
            value={parameters.mth_et_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_et_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_et_max_depth"
            value={parameters.mth_et_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_et_min_samples_split
          <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="mth_et_min_samples_split"
            value={parameters.mth_et_min_samples_split}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          mth_et_min_samples_leaf
          <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="mth_et_min_samples_leaf"
            value={parameters.mth_et_min_samples_leaf}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          mth_et_max_features
          <Tooltip text="The number of features to consider when looking for the best split. (Input: a positive integer)" />
          :
          <input
            type="number"
            name="mth_et_max_features"
            value={parameters.mth_et_max_features}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          mth_et_criterion
          <Tooltip text="It specifies the function used to measure the quality of a split in Decision Trees, Random Forest, and/or Extra Trees. (Input: “gini” or “entropy”)" />
          :
          <input
            type="text"
            name="mth_et_criterion"
            value={parameters.mth_et_criterion}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
  <label>
    mth_classifier
    <Tooltip text="Choose between XGBoost, Random Forest, Decision Tree, Extra Tree, or ALL" />
    :
    <input
      type="text"
      name="mth_classifier"
      value={parameters.mth_classifier}
      onChange={handleChange}
      className="parameter-input"
    />
  </label>
</div>
    </div>
  );
};

export default MTH;






