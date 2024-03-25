import pickle
import joblib
import xgboost as xgb
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from flask import Flask
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

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

@api.route('/LCCDE')
def run_LCCDE():
    
    # filename = 'CICIDS2017_sample1.csv'
    filename = 'CICIDS2017_sample_km1.csv'
    # Read the uploaded CSV file into a DataFrame
    print('FILE READ')
    df = pd.read_csv(filename)

    #m3.keys()
    # Split DataFrame into features (X) and labels (y)
    X = df.drop(['Label'], axis=1)
    y = df['Label']

    # Perform train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.95, test_size=0.05, random_state=0)
    m1 = joblib.load('lgb.pkl')
    m2 = xgb.XGBClassifier()
    m2.load_model('xgb_model.model')
    m3 = CatBoostClassifier()
    m3.load_model('catboost.json')
    # Call the LCCDE function with the split data
    yt, yp = LCCDE(X_test, y_test, m1, m2, m3)

    # Calculate performance metrics
    accuracy = accuracy_score(yt, yp)
    precision = precision_score(yt, yp, average='weighted')
    recall = recall_score(yt, yp, average='weighted')
    f1_average = f1_score(yt, yp, average='weighted')
    f1_per_class = f1_score(yt, yp, average=None)

    # Format the output string
    output_str = (
        f"Accuracy of LCCDE: {accuracy}\n"
        f"Precision of LCCDE: {precision}\n"
        f"Recall of LCCDE: {recall}\n"
        f"Average F1 of LCCDE: {f1_average}\n"
        f"F1 of LCCDE for each type of attack: {f1_per_class}"
    )

    return output_str


@api.route('/TreeBased')
def TreeBased():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

@api.route('/MTH')
def MTH():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

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