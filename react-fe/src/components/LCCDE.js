import React, { useState } from 'react';
import './LCCDE.css'; // Import the CSS file

const Tooltip = ({ text }) => (
  <span className="tooltip">
    <span className="tooltiptext">{text}</span>
    ?
  </span>
);

const LCCDE = () => {
  const [parameters, setParameters] = useState({
    lccde_lightgbm_learning_rate: '',
    lccde_lightgbm_num_leaves: '',
    lccde_lightgbm_n_estimators: '',
    lccde_lightgbm_max_depth: '',
    lccde_lightgbm_colsample_bytree: '',
    lccde_lightgbm_min_child_samples: '',

    lccde_xgboost_learning_rate: '',
    lccde_xgboost_max_depth: '',
    lccde_xgboost_n_estimators: '',
    lccde_xgboost_colsample_bytree: '',
    lccde_xgboost_min_child_weight: '',

    lccde_catboost_iterations: '',
    lccde_catboost_learning_rate: '',
    lccde_catboost_depth: '',
    lccde_catboost_colsample_bytree: '',
    lccde_catboost_bootstrap_type: '',
    lccde_catboost_early_stopping_rounds: '',

    lccde_classifier: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setParameters(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  return (
    <div className="lccde-container">
      <div className="parameter">
        <label>
          lccde_lightgbm_learning_rate 
          <Tooltip text="The learning rate controls how quickly the model learns from the given data. A higher learning rate will have the model learn faster but can sacrifice accuracy, while a lower learning rate will have the model learn slower but more accurately." />
          :
          <input
            type="number"
            name="lccde_lightgbm_learning_rate"
            value={parameters.lccde_lightgbm_learning_rate}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_lightgbm_num_leaves
          <Tooltip text="num_leaves represents the number of leaves for each tree. It controls the tree model’s complexity. More leaves mean the model will focus on more complex patterns and details of the data." />
          :
          <input
            type="number"
            name="lccde_lightgbm_num_leaves"
            value={parameters.lccde_lightgbm_num_leaves}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_lightgbm_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_lightgbm_n_estimators"
            value={parameters.lccde_lightgbm_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_lightgbm_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_lightgbm_max_depth"
            value={parameters.lccde_lightgbm_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          lccde_lightgbm_colsample_bytree
          <Tooltip text="This parameter determines the fraction of features when building each tree. This helps introduce randomness and reduce overfitting. It represents the variety of decision-making features the model considers at each round. More variety can help prevent the model from focusing too much on one type of feature. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="lccde_lightgbm_colsample_bytree"
            value={parameters.lccde_lightgbm_colsample_bytree}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_lightgbm_min_child_samples
          <Tooltip text="This parameter sets the minimum number of samples required in a leaf node for the model to use before making decisions. More samples can increase the model’s certainty, but too many can lead to overfitting. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_lightgbm_min_child_samples"
            value={parameters.lccde_lightgbm_min_child_samples}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          lccde_xgboost_learning_rate
          <Tooltip text="It controls how quickly the model learns from the given data. A higher learning rate will have the model learn faster but can sacrifice accuracy, while a lower learning rate will have the model learn slower but more accurately. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="lccde_xgboost_learning_rate"
            value={parameters.lccde_xgboost_learning_rate}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_xgboost_max_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_xgboost_max_depth"
            value={parameters.lccde_xgboost_max_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_xgboost_n_estimators
          <Tooltip text="n_estimators specifies the number of boosting iterations (trees) to perform in the algorithm. The number of trees is the number of chances/iterations the model gets to improve itself as it learns the data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_xgboost_n_estimators"
            value={parameters.lccde_xgboost_n_estimators}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      {/* <div className="parameter">
        <label>
          lccde_xgboost_colsample_bytree
          <Tooltip text="This determines the variety of decision-making features the model considers at each round. More variety can help prevent the model from focusing too much on one type of feature. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="lccde_xgboost_colsample_bytree"
            value={parameters.lccde_xgboost_colsample_bytree}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div> */}
      <div className="parameter">
        <label>
          lccde_xgboost_min_child_weight
          <Tooltip text="This represents the minimum weight/requirement of evidence needed for a model to make a decision. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="lccde_xgboost_min_child_weight"
            value={parameters.lccde_xgboost_min_child_weight}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_iterations
          <Tooltip text="This is how many boosting iterations (trees) of decision-making that the model can perform to improve itself. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_catboost_iterations"
            value={parameters.lccde_catboost_iterations}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_learning_rate
          <Tooltip text="The learning rate controls how quickly the model learns from the given data. A higher learning rate will have the model learn faster but can sacrifice accuracy, while a lower learning rate will have the model learn slower but more accurately. (Input: A positive real number)" />
          :
          <input
            type="number"
            name="lccde_catboost_learning_rate"
            value={parameters.lccde_catboost_learning_rate}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_depth
          <Tooltip text="This determines the maximum tree depth for each tree. It signifies how much in depth the model asks questions and makes decisions based on data. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_catboost_depth"
            value={parameters.lccde_catboost_depth}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_colsample_bytree
          <Tooltip text="This determines the variety of decision-making features the model considers at each round. More variety can help prevent the model from focusing too much on one type of feature. (Input: A real number between 0 and 1)" />
          :
          <input
            type="number"
            name="lccde_catboost_colsample_bytree"
            value={parameters.lccde_catboost_colsample_bytree}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_bootstrap_type
          <Tooltip text="This determines what bootstrap method the model will use to learn from data. Different methods affect how well a model learns. (Input: ['Bayesian', 'Bernoulli', 'MVS', 'No'])" />
          :
          <input
            type="text"
            name="lccde_catboost_bootstrap_type"
            value={parameters.lccde_catboost_bootstrap_type}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_early_stopping_rounds
          <Tooltip text="This parameter will tell a model to stop learning after a provided number of runs if the model does not improve any further. It helps prevent the model from wasting time. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="lccde_catboost_early_stopping_rounds"
            value={parameters.lccde_catboost_early_stopping_rounds}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_classifier
          <Tooltip text="Choose between lightbgm, xgboost, catboost, or all." />
          :
          <input
            type="number"
            name="lccde_classifier"
            value={parameters.lccde_classifier}
            onChange={handleChange}
            className="parameter-input"
          />
        </label>
      </div>
    </div>
  );
};

export default LCCDE;