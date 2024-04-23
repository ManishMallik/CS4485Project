from sqlalchemy import text
import random
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
import subprocess
import tree_based_ids_globecom19
import lccde_ids_globecom22
import mth_ids_iotj
app = Flask(__name__)
cors = CORS(app)

import pickle
import joblib
import xgboost as xgb
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
import gradio as gr
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score, precision_score, recall_score, f1_score
import time
from river import stream
from statistics import mode

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

#wrapper
def run_model(model, request):
    if model == 1:
        return run_LCCDE(alg_to_run = request.args["classifier"], lgb_num_leaves = int(request.args["lgbm_leaves"]), lgb_learning_rate = float(request.args["lgbm_lr"]), lgb_n_estimators = int(request.args["lgbm_n_est"]), lgb_max_depth = int(request.args["lgbm_depth"]), xgb_eta = float(request.args["xgb_lr"]), xgb_n_estimators = int(request.args["xgb_n_est"]), xgb_max_depth = int(request.args["xgb_depth"]), xgb_min_child_weight = float(request.args["xgb_min_weight"]), cb_iterations = int(request.args["cat_iter"]), cb_learning_rate = float(request.args["cat_lr"]), cb_depth = int(request.args["cat_depth"]), cb_colsample_bytree = float(request.args["cat_colsample"]), cb_bootstrap_type = request.args["cat_bs"], cb_early_stopping_rounds = int(request.args["cat_stop"]));
    elif model == 2:
        return run_TreeBased(alg_to_run = request.args["classifier"], xgb_learning_rate = float(request.args["xgb_lr"]), xgb_max_depth = (None if request.args["xgb_depth"] == "None" else int(request.args["xgb_depth"])), xgb_n_estimators = int(request.args["xgb_n_est"]), xgb_min_child_weight = float(request.args["xgb_min_weight"]), rf_n_estimators = int(request.args["rf_n_est"]), rf_max_depth = (None if request.args["rf_depth"] == "None" else int(request.args["rf_depth"])), rf_max_features = (None if request.args["rf_features"] == "None" else request.args["rf_features"]), dt_max_depth = (None if request.args["dt_depth"] else int(request.args["dt_depth"])), dt_min_samples_leaf = int(request.args["dt_leaf"]), et_n_estimators = int(request.args["et_n_est"]), et_max_depth = (None if request.args["et_depth"] == "None" else int(request.args["et_depth"])), et_min_samples_leaf = int(request.args["et_leaf"]), et_max_features = (None if request.args["et_features"] == "None" else request.args["et_features"]), dt_max_features = (None if request.args["dt_features"] == "None" else request.args["dt_features"]))
    elif model == 3:
        return run_MTH(alg_to_run = request.args["classifier"], xgb_learning_rate = float(request.args["xgb_lr"]), xgb_max_depth = (None if request.args["xgb_depth"] == "None" else int(request.args["xgb_depth"])), xgb_n_estimators = int(request.args["xgb_n_est"]), xgb_min_child_weight = float(request.args["xgb_min_weight"]), rf_n_estimators = int(request.args["rf_n_est"]), rf_max_depth = (None if request.args["rf_depth"] == "None" else int(request.args["rf_depth"])), rf_max_features = (None if request.args["rf_features"] == "None" else request.args["rf_features"]), dt_max_depth = (None if request.args["dt_depth"] else int(request.args["dt_depth"])), dt_min_samples_leaf = int(request.args["dt_leaf"]), et_n_estimators = int(request.args["et_n_est"]), et_max_depth = (None if request.args["et_depth"] == "None" else int(request.args["et_depth"])), et_min_samples_leaf = int(request.args["et_leaf"]), et_max_features = (None if request.args["et_features"] == "None" else request.args["et_features"]), dt_max_features = (None if request.args["dt_features"] == "None" else request.args["dt_features"]));
    # if model == 1:
    #     return run_LCCDE();
    # elif model == 2:
    #     return run_TreeBased()
    # elif model == 3:
    #     return run_MTH();
    
@app.route("/compare")
def compare_runs():
    f = open(".secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")
    arr = []
    with engine.connect() as conn:
        for i in conn.execute(text(f"SELECT DATE_FORMAT(time, '%Y-%m-%d %H:%i:%s') AS time, id, f1score, accuracy, `precision`, recall, model FROM Accuracy WHERE id in ({request.args.get('id1')}, {request.args.get('id2')})")).fetchall():
            dict = {}
            dict["time"] = i[0]
            dict["id"] = i[1]
            dict["f1score"] = i[2]
            dict["accuracy"] = i[3]
            dict["precision"] = i[4]
            dict["recall"] = i[5]
            dict["model"] = i[6]
            arr.append(dict)
    return arr

@app.route("/pastrun")
def pastrun():
    model_num = int(request.args["model"])
    print(model_num)
    f = open(".secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")
    dict = {}

    with engine.connect() as conn:
        for i in conn.execute(text(f"SELECT * FROM Accuracy WHERE id = {model_num}")).fetchall():
            dict["id"] = i[0]
            dict["f1score"] = i[1]
            dict["accuracy"] = i[2]
            dict["precision"] = i[3]
            dict["time"] = i[4]
            dict["recall"] = i[5]
            dict["model"] = i[6]
        print(dict)
        if int(dict["model"]) == 1:
            for i in conn.execute(text(f"SELECT * FROM LCCDE_HP WHERE id = {model_num}")).fetchall():
                dict["lgbm_lr"] = i[0]
                dict["lgbm_leaves"] = i[1]
                dict["lgbm_n_est"] = i[2]
                dict["lgbm_depth"] = i[3]
                dict["xgb_lr"] = i[4]
                dict["xgb_depth"] = i[5]
                dict["xgb_n_est"] = i[6]
                dict["xgb_min_weight"] = i[7]
                dict["cat_iter"] = i[8]
                dict["cat_lr"] = i[9]
                dict["cat_depth"] = i[10]
                dict["cat_colsample"] = i[11]
                dict["cat_bs"] = i[12]
                dict["cat_stop"] = i[13]
                dict["classifier"] = i[14]
        elif int(dict["model"]) == 2:
            for i in conn.execute(text(f"SELECT * FROM Tree_HP WHERE id = {model_num}")).fetchall():
                dict["xgb_lr"] = i[0]
                dict["xgb_depth"] = i[1]
                dict["xgb_n_est"] = i[2]
                dict["xgb_min_weight"] = i[3]
                dict["rf_n_est"] = i[4]
                dict["rf_depth"] = i[5]
                dict["rf_features"] = i[6]
                dict["dt_depth"] = i[7]
                dict["dt_leaf"] = i[8]
                dict["dt_features"] = i[9]
                dict["et_n_est"] = i[10]
                dict["et_depth"] = i[11]
                dict["et_leaf"] = i[12]
                dict["et_features"] = i[13]
                dict["classifier"] = i[14]
        elif int(dict["model"]) == 3:
            for i in conn.execute(text(f"SELECT * FROM MTH_HP WHERE id = {model_num}")).fetchall():
                dict["xgb_lr"] = i[0]
                dict["xgb_depth"] = i[1]
                dict["xgb_n_est"] = i[2]
                dict["xgb_min_weight"] = i[3]
                dict["rf_n_est"] = i[4]
                dict["rf_depth"] = i[5]
                dict["rf_features"] = i[6]
                dict["dt_depth"] = i[7]
                dict["dt_leaf"] = i[8]
                dict["dt_features"] = i[9]
                dict["et_n_est"] = i[10]
                dict["et_depth"] = i[11]
                dict["et_leaf"] = i[12]
                dict["et_features"] = i[13]
                dict["classifier"] = i[14]
    return dict

@app.route("/runmodel")
def runmodel():
    # model_type is {LCCDE, Tree Based, MST} dataset is {non_km, km}
    # step 1: information parsing
    model_num = int(request.args.get('model'))
    # step 2: run the selected model with the selected dataset
    [accuracy, precision, recall, f1_score] = run_model(model_num, request)

    # # step 3: save the output to the sql database
    f = open(".secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")

    with engine.connect() as conn:
        conn.execute(
            text(f"INSERT INTO Accuracy (f1score, accuracy, `precision`, recall, model) VALUES ({f1_score}, {accuracy}, {precision}, {recall}, {model_num})")
        )
        conn.commit()
        if model_num == 1:
            conn.execute(
                text(f"INSERT INTO LCCDE_HP VALUES (LAST_INSERT_ID(), {request.args['lgbm_lr']}, {request.args['lgbm_leaves']}, {request.args['lgbm_n_est']}, {request.args['lgbm_depth']}, {request.args['xgb_lr']}, {request.args['xgb_depth']}, {request.args['xgb_n_est']}, {request.args['xgb_min_weight']}, {request.args['cat_iter']}, {request.args['cat_lr']}, {request.args['cat_depth']}, {request.args['cat_colsample']}, '{request.args['cat_bs']}', {request.args['cat_stop']}, '{request.args['classifier']}')")
            )
        elif model_num == 2:
            conn.execute(
                text(f"INSERT INTO MTH_HP VALUES (LAST_INSERT_ID(), {request.args['xgb_lr']}, {request.args['xgb_depth']}, {request.args['xgb_n_est']}, {request.args['xgb_min_weight']}, {request.args['rf_n_est']}, {0 if request.args['rf_depth'] == 'None' else request.args['rf_depth']}, '{request.args['rf_features']}', {0 if request.args['dt_depth'] == 'None' else request.args['dt_depth']}, {request.args['dt_leaf']}, '{request.args['dt_features']}', {request.args['et_n_est']}, {0 if request.args['et_depth'] == 'None' else request.args['et_depth']}, {request.args['et_leaf']}, '{request.args['et_features']}', '{request.args['classifier']}')")
            )
        elif model_num == 3:
            conn.execute(
                text(f"INSERT INTO MTH_HP VALUES (LAST_INSERT_ID(), {request.args['xgb_lr']}, {request.args['xgb_depth']}, {request.args['xgb_n_est']}, {request.args['xgb_min_weight']}, {request.args['rf_n_est']}, {0 if request.args['rf_depth'] == 'None' else request.args['rf_depth']}, '{request.args['rf_features']}', {0 if request.args['dt_depth'] == 'None' else request.args['dt_depth']}, {request.args['dt_leaf']}, '{request.args['dt_features']}', {request.args['et_n_est']}, {0 if request.args['et_depth'] == 'None' else request.args['et_depth']}, {request.args['et_leaf']}, '{request.args['et_features']}', '{request.args['classifier']}')")
            )
        conn.commit()
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1score": f1_score}
@app.route("/getinfo")
# For past results to query all the previous results
def getinfo():
    f = open(".secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")
    arr = []
    with engine.connect() as conn:
        for i in conn.execute(text("SELECT * FROM Accuracy")).fetchall():
            dict = {}
            dict["id"] = i[0]
            dict["f1score"] = i[1]
            dict["accuracy"] = i[2]
            dict["precision"] = i[3]
            dict["time"] = i[4]
            dict["recall"] = i[5]
            dict["model"] = i[6]
            arr.append(dict)
    return arr


@app.route('/LCCDE')
def run_LCCDE(filename="CICIDS2017_sample_km.csv", alg_to_run="all",
        lgb_num_leaves=31, lgb_learning_rate=0.1, lgb_n_estimators=100, lgb_max_depth=-1, 
         lgb_min_child_samples=20, lgb_colsample_bytree=1.0,
         xgb_eta=0.3, xgb_n_estimators=10, xgb_max_depth=6,
         xgb_colsample_bytree=1.0, xgb_min_child_weight=1.0,
         cb_iterations=100, cb_learning_rate=0.03, cb_depth=6, cb_colsample_bytree=1.0,
         cb_bootstrap_type='Bayesian', cb_early_stopping_rounds=10):
    dataset = ""
    if filename == "CICIDS2017_sample_km.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample_km.csv"
    elif filename == "CICIDS2017_sample.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv"
    accuracy, precision, recall, f1_score, all_f1_scores, execution_time = lccde_ids_globecom22.main(filename=dataset, alg_to_run=alg_to_run, lgb_num_leaves=lgb_num_leaves, lgb_learning_rate=lgb_learning_rate, lgb_n_estimators=lgb_n_estimators, lgb_max_depth=lgb_max_depth, 
         lgb_min_child_samples=lgb_min_child_samples, lgb_colsample_bytree=lgb_colsample_bytree,
         xgb_eta=xgb_eta, xgb_n_estimators=xgb_n_estimators, xgb_max_depth=xgb_max_depth,
         xgb_colsample_bytree=xgb_colsample_bytree, xgb_min_child_weight=xgb_min_child_weight,
         cb_iterations=cb_iterations, cb_learning_rate=cb_learning_rate, cb_depth=cb_depth, cb_colsample_bytree=cb_colsample_bytree, cb_bootstrap_type=cb_bootstrap_type, 
         cb_early_stopping_rounds=cb_early_stopping_rounds)
    
    # return [accuracy, precision, recall, f1_score]

    # Try returning this
    return [accuracy, precision, recall, f1_score, all_f1_scores[0], all_f1_scores[1], all_f1_scores[2], all_f1_scores[3], all_f1_scores[4], all_f1_scores[5], all_f1_scores[6], execution_time]

@app.route('/TreeBased')
def run_TreeBased(filename="CICIDS2017_sample.csv", alg_to_run="all", xgb_learning_rate=0.1, xgb_max_depth=3, xgb_n_estimators=100, xgb_colsample_bytree=1, xgb_min_child_weight=1,
         rf_n_estimators=100, rf_max_depth=None, rf_min_samples_split=2, rf_min_samples_leaf=1, rf_max_features='sqrt', rf_criterion='gini',
         dt_max_depth=None, dt_min_samples_split=2, dt_min_samples_leaf=1, dt_max_features=None, dt_criterion='gini',
         et_n_estimators=100, et_max_depth=None, et_min_samples_split=2, et_min_samples_leaf=1, et_max_features='sqrt', et_criterion='gini'):
    
    dataset = ""
    if filename == "CICIDS2017_sample_km.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample_km.csv"
    elif filename == "CICIDS2017_sample.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv"

    accuracy, precision, recall, f1_score, all_f1_scores, execution_time = tree_based_ids_globecom19.main(filename=dataset, alg_to_run=alg_to_run, xgb_learning_rate=xgb_learning_rate, 
        xgb_max_depth=xgb_max_depth, xgb_n_estimators=xgb_n_estimators, xgb_colsample_bytree=xgb_colsample_bytree, xgb_min_child_weight=xgb_min_child_weight,
        rf_n_estimators=rf_n_estimators, rf_max_depth=rf_max_depth, rf_min_samples_split=rf_min_samples_split, rf_min_samples_leaf=rf_min_samples_leaf, rf_max_features=rf_max_features, 
        rf_criterion=rf_criterion, dt_max_depth=dt_max_depth, dt_min_samples_split=dt_min_samples_split, dt_min_samples_leaf=dt_min_samples_leaf, dt_max_features=dt_max_features,
        dt_criterion=dt_criterion, et_n_estimators=et_n_estimators, et_max_depth=et_max_depth, et_min_samples_split=et_min_samples_split, et_min_samples_leaf=et_min_samples_leaf,
        et_max_features=et_max_features, et_criterion=et_criterion)
    
    # return [accuracy, precision, recall, f1_score]

    # Try returning this
    return [accuracy, precision, recall, f1_score, all_f1_scores[0], all_f1_scores[1], all_f1_scores[2], all_f1_scores[3], all_f1_scores[4], all_f1_scores[5], all_f1_scores[6], execution_time]

@app.route('/MTH')
def run_MTH(filename="CICIDS2017_sample.csv", alg_to_run="all", xgb_learning_rate=0.1, xgb_max_depth=3, xgb_n_estimators=100, xgb_colsample_bytree=1, xgb_min_child_weight=1,
         rf_n_estimators=100, rf_max_depth=None, rf_min_samples_split=2, rf_min_samples_leaf=1, rf_max_features='sqrt', rf_criterion='gini',
         dt_max_depth=None, dt_min_samples_split=2, dt_min_samples_leaf=1, dt_max_features=None, dt_criterion='gini',
         et_n_estimators=100, et_max_depth=None, et_min_samples_split=2, et_min_samples_leaf=1, et_max_features='sqrt', et_criterion='gini'):
    
    dataset = ""
    if filename == "CICIDS2017_sample_km.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample_km.csv"
    elif filename == "CICIDS2017_sample.csv":
        dataset = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv"

    accuracy, precision, recall, f1_score, all_f1_scores, execution_time = mth_ids_iotj.main(filename=dataset, alg_to_run=alg_to_run, xgb_learning_rate=xgb_learning_rate, 
        xgb_max_depth=xgb_max_depth, xgb_n_estimators=xgb_n_estimators, xgb_colsample_bytree=xgb_colsample_bytree, xgb_min_child_weight=xgb_min_child_weight,
        rf_n_estimators=rf_n_estimators, rf_max_depth=rf_max_depth, rf_min_samples_split=rf_min_samples_split, rf_min_samples_leaf=rf_min_samples_leaf, rf_max_features=rf_max_features, 
        rf_criterion=rf_criterion, dt_max_depth=dt_max_depth, dt_min_samples_split=dt_min_samples_split, dt_min_samples_leaf=dt_min_samples_leaf, dt_max_features=dt_max_features,
        dt_criterion=dt_criterion, et_n_estimators=et_n_estimators, et_max_depth=et_max_depth, et_min_samples_split=et_min_samples_split, et_min_samples_leaf=et_min_samples_leaf,
        et_max_features=et_max_features, et_criterion=et_criterion)
    
    # return [accuracy, precision, recall, f1_score]

    # Try returning this
    return [accuracy, precision, recall, f1_score, all_f1_scores[0], all_f1_scores[1], all_f1_scores[2], all_f1_scores[3], all_f1_scores[4], all_f1_scores[5], all_f1_scores[6], execution_time]

if __name__ == "__main__":
    app.run()