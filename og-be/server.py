from sqlalchemy import text
import random
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
import subprocess
import tree_based_ids_globecom19
import lccde_ids_globecom22
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

with open('model_list.pkl', 'rb') as f:
    model = pickle.load(f)

#wrapper
def run_model(model_name, dataset):
    if model_name == "LCCDE":
        return run_LCCDE(dataset);
    elif model_name == "Tree Based":
        return {}
    elif model_name == "MTH":
        return {}
    


@app.route("/sendinfo")
def sendinfo():
    # model_type is {LCCDE, Tree Based, MST} dataset is {non_km, km}
    # step 1: information parsing
    model_num = int(request.args.get('model_type'))
    if model_num == 1:
        model_type = "LCCDE"
    elif model_num == 2:
        model_type = "Tree Based"
    elif model_num == 3:
        model_type = "MST"
    dataset_num = int(request.args.get('dataset'))
    if dataset_num == 1:
        dataset = "data/CICIDS2017_sample.csv"
    elif dataset_num == 2:
        dataset = "data/CICIDS2017_sample_km.csv"

    # step 2: run the selected model with the selected dataset
    output = run_model(model_type, dataset)

    # step 3: save the output to the sql database
    f = open("/home/ash/Projects/CS4485Project/og-be/.secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")
    dict = {}

    with engine.connect() as conn:
        conn.execute(
            text(f"INSERT INTO Results (model, benign, dos, portscan, bot, infiltration, webattack, bruteforce, dataset) VALUES ({model_num}, {output['benign']}, {output['dos']}, {output['portscan']}, {output['bot']}, {output['infiltration']}, {output['webattack']}, {output['bruteforce']}, {dataset_num})")
        )
        conn.commit()
        recent = conn.execute(text("SELECT DATE_FORMAT(time, '%Y-%m-%d %H:%i:%s') AS time, model, benign, bot, bruteforce, dataset, dos, id, infiltration, portscan, webattack FROM Results ORDER BY time DESC")).fetchall()[0];
        dict = {}
        dict["time"] = recent[0]
        dict["model"] = recent[1]
        dict["benign"] = recent[2]
        dict["bot"] = recent[3]
        dict["bruteforce"] = recent[4]
        dict["dataset"] = recent[5]
        dict["dos"] = recent[6]
        dict["id"] = recent[7]
        dict["infiltration"] = recent[8]
        dict["portscan"] = recent[9]
        dict["webattack"] = recent[10]
    # step 4: return the output to the front end
    return dict
@app.route("/getinfo")
# For past results to query all the previous results
def getinfo():
    f = open("/home/ash/Projects/CS4485Project/og-be/.secrets", "r")
    secret = f.read().strip()
    engine = create_engine(f"mysql+pymysql://{secret}@72.182.162.132/IDS")
    arr = []
    with engine.connect() as conn:
        for i in conn.execute(text("SELECT * FROM Results")).fetchall():
            dict = {}
            dict["id"] = i[0]
            dict["time"] = i[1]
            dict["model"] = i[2]
            dict["benign"] = i[3]
            dict["dos"] = i[4]
            dict["portscan"] = i[5]
            dict["bot"] = i[6]
            dict["infiltration"] = i[7]
            dict["webattack"] = i[8]
            dict["bruteforce"] = i[9]
            dict["dataset"] = i[10]
            arr.append(dict)
    return arr

@app.route('/Train_LCCDE')
def train_LCCDE(filename):
    if filename == "":
        filename = "https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample_km.csv"
    yp = lccde_ids_globecom22.main(filename)

# This is just a test
@app.route('/LCCDE')
def run_LCCDE(filename):
    
    # filename = 'CICIDS2017_sample1.csv'
    # filename = 'data/CICIDS2017_sample_km.csv'
    # Read the uploaded CSV file into a DataFrame
    print('FILE READ')
    df = pd.read_csv(filename)

    #m3.keys()
    # Split DataFrame into features (X) and labels (y)
    X = df.drop(['Label'], axis=1)
    y = df['Label']

    # Perform train-test split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.95, test_size=0.05, random_state=0)
    m1 = joblib.load('lgb.pkl')
    m2 = xgb.XGBClassifier()
    m2.load_model('xgb_model.model')
    m3 = CatBoostClassifier()
    m3.load_model('catboost.json')
    # Call the LCCDE function with the split data
    yt, yp = LCCDE(X, y, m1, m2, m3)

    # Calculate performance metrics
    # accuracy = accuracy_score(yt, yp)
    # precision = precision_score(yt, yp, average='weighted')
    # recall = recall_score(yt, yp, average='weighted')
    # f1_average = f1_score(yt, yp, average='weighted')
    # f1_per_class = f1_score(yt, yp, average=None)

    predict_dict = {}
    predict_dict["benign"] = 0
    predict_dict["bot"] = 0
    predict_dict["bruteforce"] = 0
    predict_dict["dos"] = 0
    predict_dict["infiltration"] = 0
    predict_dict["portscan"] = 0
    predict_dict["webattack"] = 0

    for i in yp:
        if i == 0:
            predict_dict["benign"] += 1
        elif i == 1:
            predict_dict["bot"] += 1
        elif i == 2:
            predict_dict["bruteforce"] += 1
        elif i == 3:
            predict_dict["dos"] += 1
        elif i == 4:
            predict_dict["infiltration"] += 1
        elif i == 5:
            predict_dict["portscan"] += 1
        elif i == 6:
            predict_dict["webattack"] += 1
    
    # Format the output string
    # output_str = (
    #     f"Accuracy of LCCDE: {accuracy}\n"
    #     f"Precision of LCCDE: {precision}\n"
    #     f"Recall of LCCDE: {recall}\n"
    #     f"Average F1 of LCCDE: {f1_average}\n"
    #     f"F1 of LCCDE for each type of attack: {f1_per_class}\n"
    #     f"Dictionary: {predict_dict}\n"
    # )

    return predict_dict

# Define your LCCDE function with proper model weights
def LCCDE(X_test, y_test, m1, m2, m3):
    # Rest of your function code here...
    i = 0
    t = []
    m = []
    yt = []
    yp = []
    l = []
    pred_l = []
    pro_l = []

    print("Running LCCDE")

    # For each class (normal or a type of attack), find the leader model
    for xi, yi in stream.iter_pandas(X_test, y_test):

        xi2=np.array(list(xi.values()))
        y_pred1 = m1.predict(xi2.reshape(1, -1))      # model 1 (LightGBM) makes a prediction on text sample xi
        y_pred1 = int(y_pred1[0])
        y_pred2 = m2.predict(xi2.reshape(1, -1))      # model 2 (XGBoost) makes a prediction on text sample xi
        y_pred2 = int(y_pred2[0])
        y_pred3 = m3.predict(xi2.reshape(1, -1))      # model 3 (Catboost) makes a prediction on text sample xi
        y_pred3 = int(y_pred3[0])

        p1 = m1.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 1
        p2 = m2.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 2
        p3 = m3.predict_proba(xi2.reshape(1, -1))     # The prediction probability (confidence) list of model 3

        # Find the highest prediction probability among all classes for each ML model
        y_pred_p1 = np.max(p1)
        y_pred_p2 = np.max(p2)
        y_pred_p3 = np.max(p3)

        if y_pred1 == y_pred2 == y_pred3: # If the predicted classes of all the three models are the same
            y_pred = y_pred1 # Use this predicted class as the final predicted class

        elif y_pred1 != y_pred2 != y_pred3: # If the predicted classes of all the three models are different
            # For each prediction model, check if the predicted class’s original ML model is the same as its leader model
            if model[y_pred1]==m1: # If they are the same and the leading model is model 1 (LightGBM)
                l.append(m1)
                pred_l.append(y_pred1) # Save the predicted class
                pro_l.append(y_pred_p1) # Save the confidence

            if model[y_pred2]==m2: # If they are the same and the leading model is model 2 (XGBoost)
                l.append(m2)
                pred_l.append(y_pred2)
                pro_l.append(y_pred_p2)

            if model[y_pred3]==m3: # If they are the same and the leading model is model 3 (CatBoost)
                l.append(m3)
                pred_l.append(y_pred3)
                pro_l.append(y_pred_p3)

            if len(l)==0: # Avoid empty probability list
                pro_l=[y_pred_p1,y_pred_p2,y_pred_p3]

            elif len(l)==1: # If only one pair of the original model and the leader model for each predicted class is the same
                y_pred=pred_l[0] # Use the predicted class of the leader model as the final prediction class

            else: # If no pair or multiple pairs of the original prediction model and the leader model for each predicted class are the same
                max_p = max(pro_l) # Find the highest confidence

                # Use the predicted class with the highest confidence as the final prediction class
                if max_p == y_pred_p1:
                    y_pred = y_pred1
                elif max_p == y_pred_p2:
                    y_pred = y_pred2
                else:
                    y_pred = y_pred3

        else: # If two predicted classes are the same and the other one is different
            n = mode([y_pred1,y_pred2,y_pred3]) # Find the predicted class with the majority vote
            y_pred = model[n].predict(xi2.reshape(1, -1)) # Use the predicted class of the leader model as the final prediction class
            y_pred = int(y_pred[0])

        yt.append(yi)
        yp.append(y_pred) # Save the predicted classes for all tested samples
    return yt, yp

@app.route('/TreeBased')
def run_TreeBased():

    # def run_python_script(script_path):
    #     with open(script_path, 'r') as f:
    #         script_code = f.read()
    #     exec(script_code)

    # run_python_script('tree_based_ids_globecom19.py')

    yp = tree_based_ids_globecom19.main()

    predict_dict = {}
    predict_dict["benign"] = 0
    predict_dict["bot"] = 0
    predict_dict["bruteforce"] = 0
    predict_dict["dos"] = 0
    predict_dict["infiltration"] = 0
    predict_dict["portscan"] = 0
    predict_dict["webattack"] = 0

    for key, value in yp.items():
        if key == 0:
            predict_dict["benign"] = value
        elif key == 1:
            predict_dict["bot"] = value
        elif key == 2:
            predict_dict["bruteforce"] = value
        elif key == 3:
            predict_dict["dos"] = value
        elif key == 4:
            predict_dict["infiltration"] = value
        elif key == 5:
            predict_dict["portscan"] = value
        elif key == 6:
            predict_dict["webattack"] = value

    return predict_dict
    
    # filename = 'CICIDS2017_sample1.csv'
    # df = pd.read_csv(filename)

    # #m3.keys()
    # # Split DataFrame into features (X) and labels (y)
    # X = df.drop(['Label'], axis=1)
    # y = df['Label']

    # # Perform train-test split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.95, test_size=0.05, random_state=0)

    # # Load the saved model's weights
    # loaded_model = xgb.Booster()
    # loaded_model.load_model('models/stk_model.model')

    # # The loaded model contains a stack model of DecisionTree, XgBoost. Load the DecisionTree from the loaded model
    # # dt = loaded_model['DecisionTree']

    # # Load the decision tree model
    # dt = DecisionTreeClassifier(random_state = 0)
    # dt = joblib.load('models/decision_tree_weights.pkl')
    # dt.load_model('models/decision_tree_weights.pkl')

    # # Load the random forest classifier
    # rf = RandomForestClassifier(random_state = 0)
    # rf = joblib.load('models/random_forest_weights.pkl')

    # # Load the extra tree weights
    # et = ExtraTreesClassifier(random_state = 0)
    # et = joblib.load('models/extra_tree_weights.pkl')

    # # Load the xgb
    # xgb_model = xgb.XGBClassifier()
    # xgb_model = joblib.load('models/xgb_weights.pkl')

    # # dt_train=dt.predict(X_train)
    # dt_test=dt.predict(X_test)
    # # rf_train=rf.predict(X_train)
    # rf_test=rf.predict(X_test)
    # # et_train=et.predict(X_train)
    # et_test=et.predict(X_test)
    # # xgb_train=xgb_model.predict(X_train)
    # xgb_test=xgb_model.predict(X_test)

    # # Convert the loaded model to a scikit-learn compatible format for predictions
    # xgb_sklearn_model = xgb.XGBClassifier()
    # xgb_sklearn_model._Booster = loaded_model

    # # Make predictions with the loaded model
    # y_predict_loaded = xgb_sklearn_model.predict(X_test)
    # print(y_predict_loaded)

if __name__ == "__main__":
    app.run()