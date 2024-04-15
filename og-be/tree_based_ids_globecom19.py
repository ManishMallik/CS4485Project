# # -*- coding: utf-8 -*-
# """Tree-based_IDS_GlobeCom19.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1-nTcxyZl033kNXSU9jAxmCjhnVejOLjZ

# # Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles
# This is the code for the paper entitled "[**Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles**](https://arxiv.org/pdf/1910.08635.pdf)" published in IEEE GlobeCom 2019.  
# Authors: Li Yang (liyanghart@gmail.com), Abdallah Moubayed, Ismail Hamieh, and Abdallah Shami  
# Organization: The Optimized Computing and Communications (OC2) Lab, ECE Department, Western University

# If you find this repository useful in your research, please cite:  
# L. Yang, A. Moubayed, I. Hamieh and A. Shami, "Tree-Based Intelligent Intrusion Detection System in Internet of Vehicles," 2019 IEEE Global Communications Conference (GLOBECOM), 2019, pp. 1-6, doi: 10.1109/GLOBECOM38437.2019.9013892.

# ## Import libraries
# """

# import warnings
# warnings.filterwarnings("ignore")

# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support
# from sklearn.metrics import f1_score
# from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
# from sklearn.tree import DecisionTreeClassifier
# import xgboost as xgb
# from xgboost import plot_importance
# from imblearn.over_sampling import SMOTE
# import joblib

# """## Read the sampled CICIDS2017 dataset
# The CICIDS2017 dataset is publicly available at: https://www.unb.ca/cic/datasets/ids-2017.html  
# Due to the large size of this dataset, the sampled subsets of CICIDS2017 is used. The subsets are in the "data" folder.  
# If you want to use this code on other datasets (e.g., CAN-intrusion dataset), just change the dataset name and follow the same steps. The models in this code are generic models that can be used in any intrusion detection/network traffic datasets.
# """

# def main():
#     #Read dataset
#     df = pd.read_csv('https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv')
#     # The results in this code is based on the original CICIDS2017 dataset. Please go to cell [10] if you work on the sampled dataset.

#     df

#     df.Label.value_counts()

#     """### Data sampling
#     Due to the space limit of GitHub files, we sample a small-sized subset for model learning using random sampling
#     """

#     # Randomly sample instances from majority classes
#     df_minor = df[(df['Label']=='WebAttack')|(df['Label']=='Bot')|(df['Label']=='Infiltration')]
#     df_BENIGN = df[(df['Label']=='BENIGN')]
#     df_BENIGN = df_BENIGN.sample(n=None, frac=0.01, replace=False, weights=None, random_state=None, axis=0)
#     df_DoS = df[(df['Label']=='DoS')]
#     df_DoS = df_DoS.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
#     df_PortScan = df[(df['Label']=='PortScan')]
#     df_PortScan = df_PortScan.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
#     df_BruteForce = df[(df['Label']=='BruteForce')]
#     df_BruteForce = df_BruteForce.sample(n=None, frac=0.2, replace=False, weights=None, random_state=None, axis=0)

#     df_s = df_BENIGN.append(df_DoS).append(df_PortScan).append(df_BruteForce).append(df_minor)

#     df_s = df_s.sort_index()

#     # Save the sampled dataset
#     df_s.to_csv('data/CICIDS2017_sample.csv',index=0)

#     """### Preprocessing (normalization and padding values)"""

#     df = pd.read_csv('data/CICIDS2017_sample.csv')

#     # Min-max normalization
#     numeric_features = df.dtypes[df.dtypes != 'object'].index
#     df[numeric_features] = df[numeric_features].apply(
#         lambda x: (x - x.min()) / (x.max()-x.min()))
#     # Fill empty values by 0
#     df = df.fillna(0)

#     """### split train set and test set"""

#     labelencoder = LabelEncoder()
#     df.iloc[:, -1] = labelencoder.fit_transform(df.iloc[:, -1])
#     X = df.drop(['Label'],axis=1).values
#     y = df.iloc[:, -1].values.reshape(-1,1)
#     y=np.ravel(y)
#     X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

#     X_train.shape

#     pd.Series(y_train).value_counts()

#     """### Oversampling by SMOTE"""

#     smote=SMOTE(n_jobs=-1,sampling_strategy={4:1500}) # Create 1500 samples for the minority class "4"

#     X_train, y_train = smote.fit_resample(X_train, y_train)

#     pd.Series(y_train).value_counts()

#     """## Machine learning model training

#     ### Training four base learners: decision tree, random forest, extra trees, XGBoost
#     """

#     # Decision tree training and prediction
#     dt = DecisionTreeClassifier(random_state = 0)
#     dt.fit(X_train,y_train)
#     dt_score=dt.score(X_test,y_test)
#     y_predict=dt.predict(X_test)
#     y_true=y_test
#     print('Accuracy of DT: '+ str(dt_score))
#     precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     print('Precision of DT: '+(str(precision)))
#     print('Recall of DT: '+(str(recall)))
#     print('F1-score of DT: '+(str(fscore)))
#     print(classification_report(y_true,y_predict))
#     cm=confusion_matrix(y_true,y_predict)
#     f,ax=plt.subplots(figsize=(5,5))
#     sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     plt.xlabel("y_pred")
#     plt.ylabel("y_true")
#     #plt.show()

#     dt_train=dt.predict(X_train)
#     dt_test=dt.predict(X_test)

#     # Random Forest training and prediction
#     rf = RandomForestClassifier(random_state = 0)
#     rf.fit(X_train,y_train)
#     rf_score=rf.score(X_test,y_test)
#     y_predict=rf.predict(X_test)
#     y_true=y_test
#     print('Accuracy of RF: '+ str(rf_score))
#     precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     print('Precision of RF: '+(str(precision)))
#     print('Recall of RF: '+(str(recall)))
#     print('F1-score of RF: '+(str(fscore)))
#     print(classification_report(y_true,y_predict))
#     cm=confusion_matrix(y_true,y_predict)
#     f,ax=plt.subplots(figsize=(5,5))
#     sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     plt.xlabel("y_pred")
#     plt.ylabel("y_true")
#     #plt.show()

#     rf_train=rf.predict(X_train)
#     rf_test=rf.predict(X_test)

#     # Extra trees training and prediction
#     et = ExtraTreesClassifier(random_state = 0)
#     et.fit(X_train,y_train)
#     et_score=et.score(X_test,y_test)
#     y_predict=et.predict(X_test)
#     y_true=y_test
#     print('Accuracy of ET: '+ str(et_score))
#     precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     print('Precision of ET: '+(str(precision)))
#     print('Recall of ET: '+(str(recall)))
#     print('F1-score of ET: '+(str(fscore)))
#     print(classification_report(y_true,y_predict))
#     cm=confusion_matrix(y_true,y_predict)
#     f,ax=plt.subplots(figsize=(5,5))
#     sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     plt.xlabel("y_pred")
#     plt.ylabel("y_true")
#     #plt.show()

#     et_train=et.predict(X_train)
#     et_test=et.predict(X_test)

#     # XGboost training and prediction
#     xg = xgb.XGBClassifier(n_estimators = 10)
#     xg.fit(X_train,y_train)
#     xg_score=xg.score(X_test,y_test)
#     y_predict=xg.predict(X_test)
#     y_true=y_test
#     print('Accuracy of XGBoost: '+ str(xg_score))
#     precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     print('Precision of XGBoost: '+(str(precision)))
#     print('Recall of XGBoost: '+(str(recall)))
#     print('F1-score of XGBoost: '+(str(fscore)))
#     print(classification_report(y_true,y_predict))
#     cm=confusion_matrix(y_true,y_predict)
#     f,ax=plt.subplots(figsize=(5,5))
#     sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     plt.xlabel("y_pred")
#     plt.ylabel("y_true")
#     #plt.show()

#     xg_train=xg.predict(X_train)
#     xg_test=xg.predict(X_test)

#     # """### Stacking model construction (ensemble for 4 base learners)"""

#     # # Use the outputs of 4 base models to construct a new ensemble model
#     # base_predictions_train = pd.DataFrame( {
#     #     'DecisionTree': dt_train.ravel(),
#     #         'RandomForest': rf_train.ravel(),
#     #     'ExtraTrees': et_train.ravel(),
#     #     'XgBoost': xg_train.ravel(),
#     #     })
#     # base_predictions_train.head(5)

#     # dt_train=dt_train.reshape(-1, 1)
#     # et_train=et_train.reshape(-1, 1)
#     # rf_train=rf_train.reshape(-1, 1)
#     # xg_train=xg_train.reshape(-1, 1)
#     # dt_test=dt_test.reshape(-1, 1)
#     # et_test=et_test.reshape(-1, 1)
#     # rf_test=rf_test.reshape(-1, 1)
#     # xg_test=xg_test.reshape(-1, 1)

#     # x_train = np.concatenate(( dt_train, et_train, rf_train, xg_train), axis=1)
#     # x_test = np.concatenate(( dt_test, et_test, rf_test, xg_test), axis=1)

#     # stk = xgb.XGBClassifier().fit(x_train, y_train)

#     # y_predict=stk.predict(x_test)
#     # y_true=y_test
#     # stk_score=accuracy_score(y_true,y_predict)
#     # print('Accuracy of Stacking: '+ str(stk_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of Stacking: '+(str(precision)))
#     # print('Recall of Stacking: '+(str(recall)))
#     # print('F1-score of Stacking: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     # #plt.show()

#     # """## Feature Selection

#     # ### Feature importance
#     # """

#     # # Save the feature importance lists generated by four tree-based algorithms
#     # dt_feature = dt.feature_importances_
#     # rf_feature = rf.feature_importances_
#     # et_feature = et.feature_importances_
#     # xgb_feature = xg.feature_importances_

#     # # calculate the average importance value of each feature
#     # avg_feature = (dt_feature + rf_feature + et_feature + xgb_feature)/4

#     # feature=(df.drop(['Label'],axis=1)).columns.values
#     # print ("Features sorted by their score:")
#     # print (sorted(zip(map(lambda x: round(x, 4), avg_feature), feature), reverse=True))

#     # f_list = sorted(zip(map(lambda x: round(x, 4), avg_feature), feature), reverse=True)

#     # len(f_list)

#     # # Select the important features from top-importance to bottom-importance until the accumulated importance reaches 0.9 (out of 1)
#     # Sum = 0
#     # fs = []
#     # for i in range(0, len(f_list)):
#     #     Sum = Sum + f_list[i][0]
#     #     fs.append(f_list[i][1])
#     #     if Sum>=0.9:
#     #         break

#     # X_fs = df[fs].values

#     # X_train, X_test, y_train, y_test = train_test_split(X_fs,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

#     # X_train.shape

#     # pd.Series(y_train).value_counts()

#     # """### Oversampling by SMOTE"""

#     # smote=SMOTE(n_jobs=-1,sampling_strategy={4:1500})

#     # X_train, y_train = smote.fit_resample(X_train, y_train)

#     # pd.Series(y_train).value_counts()

#     # """## Machine learning model training after feature selection"""

#     # dt = DecisionTreeClassifier(random_state = 0)
#     # dt.fit(X_train,y_train)
#     # dt_score=dt.score(X_test,y_test)
#     # y_predict=dt.predict(X_test)
#     # y_true=y_test
#     # print('Accuracy of DT: '+ str(dt_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of DT: '+(str(precision)))
#     # print('Recall of DT: '+(str(recall)))
#     # print('F1-score of DT: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     # #plt.show()

#     # # Save the trained model weights to a file
#     # joblib.dump(dt, 'decision_tree_weights.pkl')

#     # dt_train=dt.predict(X_train)
#     # dt_test=dt.predict(X_test)

#     # rf = RandomForestClassifier(random_state = 0)
#     # rf.fit(X_train,y_train) # modelin veri üzerinde öğrenmesi fit fonksiyonuyla yapılıyor
#     # rf_score=rf.score(X_test,y_test)
#     # y_predict=rf.predict(X_test)
#     # y_true=y_test
#     # print('Accuracy of RF: '+ str(rf_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of RF: '+(str(precision)))
#     # print('Recall of RF: '+(str(recall)))
#     # print('F1-score of RF: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     # #plt.show()

#     # joblib.dump(rf, 'random_forest_weights.pkl')

#     # rf_train=rf.predict(X_train)
#     # rf_test=rf.predict(X_test)

#     # et = ExtraTreesClassifier(random_state = 0)
#     # et.fit(X_train,y_train)
#     # et_score=et.score(X_test,y_test)
#     # y_predict=et.predict(X_test)
#     # y_true=y_test
#     # print('Accuracy of ET: '+ str(et_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of ET: '+(str(precision)))
#     # print('Recall of ET: '+(str(recall)))
#     # print('F1-score of ET: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     # #plt.show()

#     # joblib.dump(et, 'extra_trees_weights.pkl')

#     # et_train=et.predict(X_train)
#     # et_test=et.predict(X_test)

#     # xg = xgb.XGBClassifier(n_estimators = 10)
#     # xg.fit(X_train,y_train)
#     # xg_score=xg.score(X_test,y_test)
#     # y_predict=xg.predict(X_test)
#     # y_true=y_test
#     # print('Accuracy of XGBoost: '+ str(xg_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of XGBoost: '+(str(precision)))
#     # print('Recall of XGBoost: '+(str(recall)))
#     # print('F1-score of XGBoost: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     # #plt.show()

#     # joblib.dump(xg, 'xg_boost_weights.pkl')

#     # xg_train=xg.predict(X_train)
#     # xg_test=xg.predict(X_test)

#     # """### Stacking model construction"""

#     # base_predictions_train = pd.DataFrame( {
#     #     'DecisionTree': dt_train.ravel(),
#     #         'RandomForest': rf_train.ravel(),
#     #     'ExtraTrees': et_train.ravel(),
#     #     'XgBoost': xg_train.ravel(),
#     #     })
#     # base_predictions_train.head(5)

#     # dt_train=dt_train.reshape(-1, 1)
#     # et_train=et_train.reshape(-1, 1)
#     # rf_train=rf_train.reshape(-1, 1)
#     # xg_train=xg_train.reshape(-1, 1)
#     # dt_test=dt_test.reshape(-1, 1)
#     # et_test=et_test.reshape(-1, 1)
#     # rf_test=rf_test.reshape(-1, 1)
#     # xg_test=xg_test.reshape(-1, 1)

#     # x_train = np.concatenate(( dt_train, et_train, rf_train, xg_train), axis=1)
#     # x_test = np.concatenate(( dt_test, et_test, rf_test, xg_test), axis=1)

#     # x_test

#     # stk = xgb.XGBClassifier().fit(x_train, y_train)
#     # y_predict=stk.predict(x_test)
#     # y_true=y_test
#     # stk_score=accuracy_score(y_true,y_predict)
#     # print('Accuracy of Stacking: '+ str(stk_score))
#     # precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
#     # print('Precision of Stacking: '+(str(precision)))
#     # print('Recall of Stacking: '+(str(recall)))
#     # print('F1-score of Stacking: '+(str(fscore)))
#     # print(classification_report(y_true,y_predict))
#     # cm=confusion_matrix(y_true,y_predict)
#     # f,ax=plt.subplots(figsize=(5,5))
#     # sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
#     # plt.xlabel("y_pred")
#     # plt.ylabel("y_true")
#     #plt.show()

#     # print("Predicted Labels:")
#     # for label in y_predict:
#     #     print(label)

#     return convert_to_dict(y_predict)

# from collections import Counter

# def convert_to_dict(y_predict):
#     # Count the occurrences of each label
#     label_counts = Counter(y_predict)

#     # Convert the Counter object to a dictionary
#     label_dict = {int(key): value for key, value in label_counts.items()}

#     return label_dict


#     # stk.save_model('stk_model.model')

#     # # Load the saved model's weights
#     # loaded_model = xgb.XGBClassifier()
#     # loaded_model.load_model('/content/stk_model.model')

#     # # Make predictions with the loaded model
#     # y_predict_loaded = loaded_model.predict(x_test)

#     # #Read dataset
#     # dffff = pd.read_csv('https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv')
#     # # The results in this code is based on the original CICIDS2017 dataset. Please go to cell [10] if you work on the sampled dataset.

#     # labelencoder = LabelEncoder()
#     # dffff.iloc[:, -1] = labelencoder.fit_transform(dffff.iloc[:, -1])
#     # X = df.drop(['Label'],axis=1).values
#     # y = df.iloc[:, -1].values.reshape(-1,1)
#     # y=np.ravel(y)
#     # X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

#     # Load the saved model's weights
#     # loaded_dt = DecisionTreeClassifier(random_state = 0)
#     # loaded_dt = joblib.load('/content/decision_tree_weights.pkl')

#     # # Make predictions with the loaded model
#     # y_predict_loaded = loaded_dt.predict(X_train)

#     # # Load the saved model's weights
#     # loaded_et = ExtraTreesClassifier(random_state = 0)
#     # loaded_et = joblib.load('/content/extra_trees_weights.pkl')

#     # # Make predictions with the loaded model
#     # #y_predict_et = loaded_et.predict(x_test)

#     # # Load the saved model's weights
#     # loaded_rf = RandomForestClassifier(random_state = 0)
#     # loaded_rf = joblib.load('/content/random_forest_weights.pkl')

#     # # Make predictions with the loaded model
#     # #y_predict_rf = loaded_rf.predict(x_test)

#     # # Load the saved model's weights
#     # loaded_xg = xgb.XGBClassifier()
#     # loaded_xg.load_model('/content/xg_boost_weights.pkl')

#     # # Make predictions with the loaded model
#     # y_predict_xg = loaded_xg.predict(x_test)

#     # for label in y_predict_loaded:
#     #     print(label)

# if __name__ == "__main__":
#     main()
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost import plot_importance
from imblearn.over_sampling import SMOTE
import joblib

def main(alg_to_run="all", xgb_learning_rate=0.1, xgb_max_depth=3, xgb_n_estimators=100, xgb_colsample_bytree=1, xgb_min_child_weight=1,
         rf_n_estimators=100, rf_max_depth=None, rf_min_samples_split=2, rf_min_samples_leaf=1, rf_max_features='sqrt', rf_criterion='gini',
         dt_max_depth=None, dt_min_samples_split=2, dt_min_samples_leaf=1, dt_max_features=None, dt_criterion='gini',
         et_n_estimators=100, et_max_depth=None, et_min_samples_split=2, et_min_samples_leaf=1, et_max_features='sqrt', et_criterion='gini'):
    # Read dataset
    df = pd.read_csv('https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv')
    
    # Data sampling
    df_minor = df[(df['Label'] == 'WebAttack') | (df['Label'] == 'Bot') | (df['Label'] == 'Infiltration')]
    df_BENIGN = df[(df['Label'] == 'BENIGN')]
    df_BENIGN = df_BENIGN.sample(n=None, frac=0.01, replace=False, weights=None, random_state=None, axis=0)
    df_DoS = df[(df['Label'] == 'DoS')]
    df_DoS = df_DoS.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
    df_PortScan = df[(df['Label'] == 'PortScan')]
    df_PortScan = df_PortScan.sample(n=None, frac=0.05, replace=False, weights=None, random_state=None, axis=0)
    df_BruteForce = df[(df['Label'] == 'BruteForce')]
    df_BruteForce = df_BruteForce.sample(n=None, frac=0.2, replace=False, weights=None, random_state=None, axis=0)

    df_s = df_BENIGN.append(df_DoS).append(df_PortScan).append(df_BruteForce).append(df_minor)
    df_s = df_s.sort_index()

    # Save the sampled dataset
    df_s.to_csv('data/CICIDS2017_sample.csv', index=0)

    # Preprocessing (normalization and padding values)
    df = pd.read_csv('data/CICIDS2017_sample.csv')

    # Min-max normalization
    numeric_features = df.dtypes[df.dtypes != 'object'].index
    df[numeric_features] = df[numeric_features].apply(lambda x: (x - x.min()) / (x.max()-x.min()))
    # Fill empty values by 0
    df = df.fillna(0)

    # split train set and test set
    labelencoder = LabelEncoder()
    df.iloc[:, -1] = labelencoder.fit_transform(df.iloc[:, -1])
    X = df.drop(['Label'], axis=1).values
    y = df.iloc[:, -1].values.reshape(-1,1)
    y = np.ravel(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0, stratify=y)

    # Oversampling by SMOTE
    smote = SMOTE(n_jobs=-1, sampling_strategy={4: 1500})  # Create 1500 samples for the minority class "4"
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Machine learning model training

    # Decision tree training and prediction
    dt = DecisionTreeClassifier(max_depth=dt_max_depth, min_samples_split=dt_min_samples_split, min_samples_leaf=dt_min_samples_leaf,
                                 max_features=dt_max_features, criterion=dt_criterion, random_state=0)
    dt.fit(X_train, y_train)
    dt_score = dt.score(X_test, y_test)
    y_predict = dt.predict(X_test)
    dt_predict = y_predict
    y_true = y_test
    print('Accuracy of DT: ' + str(dt_score))
    precision, recall, fscore, none = precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of DT: ' + str(precision))
    print('Recall of DT: ' + str(recall))
    print('F1-score of DT: ' + str(fscore))
    dt_fscore = fscore
    print(classification_report(y_true, y_predict))
    cm = confusion_matrix(y_true, y_predict)
    f, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")

    # Random Forest training and prediction
    rf = RandomForestClassifier(n_estimators=rf_n_estimators, max_depth=rf_max_depth, min_samples_split=rf_min_samples_split,
                                 min_samples_leaf=rf_min_samples_leaf, max_features=rf_max_features, criterion=rf_criterion, random_state=0)
    rf.fit(X_train, y_train)
    rf_score = rf.score(X_test, y_test)
    y_predict = rf.predict(X_test)
    rf_predict = y_predict
    y_true = y_test
    print('Accuracy of RF: ' + str(rf_score))
    precision, recall, fscore, none = precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of RF: ' + str(precision))
    print('Recall of RF: ' + str(recall))
    print('F1-score of RF: ' + str(fscore))
    rf_fscore = fscore
    print(classification_report(y_true, y_predict))
    cm = confusion_matrix(y_true, y_predict)
    f, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")

    # Extra Trees training and prediction
    et = ExtraTreesClassifier(n_estimators=et_n_estimators, max_depth=et_max_depth, min_samples_split=et_min_samples_split,
                              min_samples_leaf=et_min_samples_leaf, max_features=et_max_features, criterion=et_criterion, random_state=0)
    et.fit(X_train, y_train)
    et_score = et.score(X_test, y_test)
    y_predict = et.predict(X_test)
    et_predict = y_predict
    y_true = y_test
    print('Accuracy of ET: ' + str(et_score))
    precision, recall, fscore, none = precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of ET: ' + str(precision))
    print('Recall of ET: ' + str(recall))
    print('F1-score of ET: ' + str(fscore))
    et_fscore = fscore
    print(classification_report(y_true, y_predict))
    cm = confusion_matrix(y_true, y_predict)
    f, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")

    # XGBoost training and prediction
    xg = xgb.XGBClassifier(learning_rate=xgb_learning_rate, max_depth=xgb_max_depth, n_estimators=xgb_n_estimators,
                           colsample_bytree=xgb_colsample_bytree, min_child_weight=xgb_min_child_weight)
    xg.fit(X_train, y_train)
    xg_score = xg.score(X_test, y_test)
    y_predict = xg.predict(X_test)
    xg_predict = y_predict
    y_true = y_test
    print('Accuracy of XGBoost: ' + str(xg_score))
    precision, recall, fscore, none = precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of XGBoost: ' + str(precision))
    print('Recall of XGBoost: ' + str(recall))
    print('F1-score of XGBoost: ' + str(fscore))
    xg_fscore = fscore
    print(classification_report(y_true, y_predict))
    cm = confusion_matrix(y_true, y_predict)
    f, ax = plt.subplots(figsize=(5, 5))
    sns.heatmap(cm, annot=True, linewidth=0.5, linecolor="red", fmt=".0f", ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")

    if alg_to_run == "decision tree":
        #print the accuracy, precision, and f1 score of the decision tree model
        print('Accuracy of DT: ' + str(dt_score))
        precision, recall, fscore, none = precision_recall_fscore_support(y_true, dt_predict, average='weighted')
        print('Precision of DT: ' + str(precision))
        print('Recall of DT: ' + str(recall))
        print('F1-score of DT: ' + str(fscore))
        return dt_score, precision, recall, fscore
    elif alg_to_run == "random forest":
        #print the accuracy, precision, and f1 score of the random forest model
        print('Accuracy of RF: ' + str(rf_score))
        precision, recall, fscore, none = precision_recall_fscore_support(y_true, rf_predict, average='weighted')
        print('Precision of RF: ' + str(precision))
        print('Recall of RF: ' + str(recall))
        print('F1-score of RF: ' + str(fscore))
        return rf_score, precision, recall, fscore
    elif alg_to_run == "extra trees":
        #print the accuracy, precision, and f1 score of the extra trees model
        print('Accuracy of ET: ' + str(et_score))
        precision, recall, fscore, none = precision_recall_fscore_support(y_true, et_predict, average='weighted')
        print('Precision of ET: ' + str(precision))
        print('Recall of ET: ' + str(recall))
        print('F1-score of ET: ' + str(fscore))
        return et_score, precision, recall, fscore
    elif alg_to_run == "xgboost":
        #print the accuracy, precision, and f1 score of the xgboost model
        print('Accuracy of XGBoost: ' + str(xg_score))
        precision, recall, fscore, none = precision_recall_fscore_support(y_true, xg_predict, average='weighted')
        print('Precision of XGBoost: ' + str(precision))
        print('Recall of XGBoost: ' + str(recall))
        print('F1-score of XGBoost: ' + str(fscore))
        return xg_score, precision, recall, fscore
    else:

        # get the model with the max average f1_score
        model_fscores = {"Decision Tree": dt_fscore, "Random Forest": rf_fscore, "Extra Trees": et_fscore, "XGBoost": xg_fscore}
        best_model = max(model_fscores, key=model_fscores.get)

        #find the model with the max accuracy, then print out that model's accuracy, precision, and f1 score
        # model_scores = {"Decision Tree": dt_score, "Random Forest": rf_score, "Extra Trees": et_score, "XGBoost": xg_score}
        # best_model = max(model_scores, key=model_scores.get)
        print('Best model: ' + best_model)
        #print the best_model accuracy, recall, and f1 score
        if best_model == "Decision Tree":
            accuracy = dt_score
            precision, recall, fscore, none = precision_recall_fscore_support(y_true, dt_predict, average='weighted')
        elif best_model == "Random Forest":
            accuracy = rf_score
            precision, recall, fscore, none = precision_recall_fscore_support(y_true, rf_predict, average='weighted')
        elif best_model == "Extra Trees":
            accuracy = et_score
            precision, recall, fscore, none = precision_recall_fscore_support(y_true, et_predict, average='weighted')
        else:
            accuracy = xg_score
            precision, recall, fscore, none = precision_recall_fscore_support(y_true, xg_predict, average='weighted')
        print('Accuracy of ' + best_model + ': ' + str(accuracy))
        print('Precision of ' + best_model + ': ' + str(precision))
        print('Recall of ' + best_model + ': ' + str(recall))
        print('F1-score of ' + best_model + ': ' + str(model_fscores[best_model]))
        return accuracy, precision, recall, model_fscores[best_model]
    
if __name__ == "__main__":
    main()
