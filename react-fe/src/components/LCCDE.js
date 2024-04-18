import React, { useEffect, useState } from 'react';
import './LCCDE.css'; // Import the CSS file

const Tooltip = ({ text }) => (
  <span className="tooltip">
    <span className="tooltiptext">{text}</span>
    ?
  </span>
);

const LCCDE = (props) => {
  const [parameters, setParameters] = useState({
    lgbm_lr: '0.1',
    lgbm_leaves: '31',
    lgbm_n_est: '100',
    lgbm_depth: '1',

    xgb_lr: '0.3',
    xgb_depth: '6',
    xgb_n_est: '10',
    xgb_min_weight: '1.0',

    cat_iter: '100',
    cat_lr: '0.03',
    cat_depth: '6',
    cat_colsample: '1.0',
    cat_bs: 'Bayesian',
    cat_stop: '10',

    classifier: 'all'
  });
  useEffect(()=>{
    props.setData(parameters)
  }, [parameters])

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Input validation for positive integers
    if (name.includes('leaves') || name.includes('_n_est') || name.includes('depth') ||
        name.includes('_min_child_samples') || name.includes('_iter') || name.includes('_depth') ||
        name.includes('stop')) {
      if (!/^\d+$/.test(value) && value !== "") {
        // Not a positive integer, show error
        alert('Please enter a positive integer.');
        return;
      }
    }

    if (name === "cat_colsample") {
      const floatValue = parseFloat(value);
      if (value !== "" && (isNaN(floatValue) || floatValue < 0 || floatValue > 1)) {
        // Not a valid value, show error
        alert("Please enter a number between 0 and 1.");
        return;
      }
    }

    setParameters(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleDropdownChange = (e) => {
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
            name="lgbm_lr"
            value={parameters.lgbm_lr}
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
            name="lgbm_leaves"
            value={parameters.lgbm_leaves}
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
            name="lgbm_n_est"
            value={parameters.lgbm_n_est}
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
            name="lgbm_depth"
            value={parameters.lgbm_depth}
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
            name="xgb_lr"
            value={parameters.xgb_lr}
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
            name="xgb_depth"
            value={parameters.xgb_depth}
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
            name="xgb_n_est"
            value={parameters.xgb_n_est}
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
            name="xgb_min_weight"
            value={parameters.xgb_min_weight}
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
            name="cat_iter"
            value={parameters.cat_iter}
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
            name="cat_lr"
            value={parameters.cat_lr}
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
            name="cat_depth"
            value={parameters.cat_depth}
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
            name="cat_colsample"
            value={parameters.cat_colsample}
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
          <select
            name="cat_bs"
            value={parameters.cat_bs}
            onChange={handleDropdownChange}
            className="parameter-input"
          >
            <option value="Bayesian">Bayesian</option>
            <option value="Bernoulli">Bernoulli</option>
            <option value="MVS">MVS</option>
            <option value="No">No</option>
          </select>
        </label>
      </div>
      <div className="parameter">
        <label>
          lccde_catboost_early_stopping_rounds
          <Tooltip text="This parameter will tell a model to stop learning after a provided number of runs if the model does not improve any further. It helps prevent the model from wasting time. (Input: A positive integer)" />
          :
          <input
            type="number"
            name="cat_stop"
            value={parameters.cat_stop}
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
          <select
            name="classifier"
            value={parameters.classifier}
            onChange={handleDropdownChange}
            className="parameter-input"
          >
            <option value="all">all</option>
            <option value="lightbgm">lightbgm</option>
            <option value="xgboost">xgboost</option>
            <option value="catboost">catboost</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default LCCDE;