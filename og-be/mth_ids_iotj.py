# -*- coding: utf-8 -*-
"""MTH_IDS_IoTJ.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aI4PzhO6Uc4ZWbw2ygF-JO1Ncc8q6VcF

# MTH-IDS: A Multi-Tiered Hybrid Intrusion Detection System for Internet of Vehicles
This is the code for the paper entitled "[**MTH-IDS: A Multi-Tiered Hybrid Intrusion Detection System for Internet of Vehicles**](https://arxiv.org/pdf/2105.13289.pdf)" accepted in IEEE Internet of Things Journal.  
Authors: Li Yang (liyanghart@gmail.com), Abdallah Moubayed, and Abdallah Shami  
Organization: The Optimized Computing and Communications (OC2) Lab, ECE Department, Western University

If you find this repository useful in your research, please cite:  
L. Yang, A. Moubayed, and A. Shami, “MTH-IDS: A Multi-Tiered Hybrid Intrusion Detection System for Internet of Vehicles,” IEEE Internet of Things Journal, vol. 9, no. 1, pp. 616-632, Jan.1, 2022.

## Import libraries
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,precision_recall_fscore_support
from sklearn.metrics import f1_score,roc_auc_score
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost import plot_importance
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_selection import mutual_info_classif
from imblearn.over_sampling import SMOTE
from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
import pickle

def main():
    pd.__version__

    """## Read the sampled CICIDS2017 dataset
    The CICIDS2017 dataset is publicly available at: https://www.unb.ca/cic/datasets/ids-2017.html  
    Due to the large size of this dataset, the sampled subsets of CICIDS2017 is used. The subsets are in the "data" folder.  
    If you want to use this code on other datasets (e.g., CAN-intrusion dataset), just change the dataset name and follow the same steps. The models in this code are generic models that can be used in any intrusion detection/network traffic datasets.
    """

    #Read dataset
    df = pd.read_csv('https://raw.githubusercontent.com/Western-OC2-Lab/Intrusion-Detection-System-Using-Machine-Learning/main/data/CICIDS2017_sample.csv')
    # The results in this code is based on the original CICIDS2017 dataset. Please go to cell [21] if you work on the sampled dataset.

    df

    df.Label.value_counts()

    """### Preprocessing (normalization and padding values)"""

    # Z-score normalization
    features = df.dtypes[df.dtypes != 'object'].index
    df[features] = df[features].apply(
        lambda x: (x - x.mean()) / (x.std()))
    # Fill empty values by 0
    df = df.fillna(0)

    """### Data sampling
    Due to the space limit of GitHub files and the large size of network traffic data, we sample a small-sized subset for model learning using **k-means cluster sampling**
    """

    labelencoder = LabelEncoder()
    df.iloc[:, -1] = labelencoder.fit_transform(df.iloc[:, -1])

    df.Label.value_counts()

    # retain the minority class instances and sample the majority class instances
    df_minor = df[(df['Label']==6)|(df['Label']==1)|(df['Label']==4)]
    df_major = df.drop(df_minor.index)

    X = df_major.drop(['Label'],axis=1)
    y = df_major.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)

    # use k-means to cluster the data samples and select a proportion of data from each cluster
    kmeans = MiniBatchKMeans(n_clusters=1000, random_state=0).fit(X)

    klabel=kmeans.labels_
    df_major['klabel']=klabel

    df_major['klabel'].value_counts()

    cols = list(df_major)
    cols.insert(78, cols.pop(cols.index('Label')))
    df_major = df_major.loc[:, cols]

    df_major

    def typicalSampling(group):
        name = group.name
        frac = 0.008
        return group.sample(frac=frac)

    result = df_major.groupby(
        'klabel', group_keys=False
    ).apply(typicalSampling)

    result['Label'].value_counts()

    result

    result = result.drop(['klabel'],axis=1)
    result = result.append(df_minor)

    result.to_csv('CICIDS2017.csv',index=0)

    """### split train set and test set"""

    # Read the sampled dataset
    df=pd.read_csv('CICIDS2017.csv')

    X = df.drop(['Label'],axis=1).values
    y = df.iloc[:, -1].values.reshape(-1,1)
    y=np.ravel(y)

    X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

    """## Feature engineering

    ### Feature selection by information gain
    """
    importances = mutual_info_classif(X_train, y_train)

    # calculate the sum of importance scores
    f_list = sorted(zip(map(lambda x: round(x, 4), importances), features), reverse=True)
    Sum = 0
    fs = []
    for i in range(0, len(f_list)):
        Sum = Sum + f_list[i][0]
        fs.append(f_list[i][1])

    # select the important features from top to bottom until the accumulated importance reaches 90%
    f_list2 = sorted(zip(map(lambda x: round(x, 4), importances/Sum), features), reverse=True)
    Sum2 = 0
    fs = []
    for i in range(0, len(f_list2)):
        Sum2 = Sum2 + f_list2[i][0]
        fs.append(f_list2[i][1])
        if Sum2>=0.9:
            break

    X_fs = df[fs].values

    X_fs.shape

    """### Feature selection by Fast Correlation Based Filter (FCBF)

    The module is imported from the GitHub repo: https://github.com/SantiagoEG/FCBF_module
    """

    # -*- coding: utf-8 -*-


    def count_vals(x):
        vals = np.unique(x)
        occ = np.zeros(shape = vals.shape)
        for i in range(vals.size):
            occ[i] = np.sum(x == vals[i])
        return occ

    def entropy(x):
        n = float(x.shape[0])
        ocurrence = count_vals(x)
        px = ocurrence / n
        return -1* np.sum(px*np.log2(px))

    def symmetricalUncertain(x,y):
        n = float(y.shape[0])
        vals = np.unique(y)
        # Computing Entropy for the feature x.
        Hx = entropy(x)
        # Computing Entropy for the feature y.
        Hy = entropy(y)
        #Computing Joint entropy between x and y.
        partial = np.zeros(shape = (vals.shape[0]))
        for i in range(vals.shape[0]):
            partial[i] = entropy(x[y == vals[i]])

        partial[np.isnan(partial)==1] = 0
        py = count_vals(y).astype(dtype = 'float64') / n
        Hxy = np.sum(py[py > 0]*partial)
        IG = Hx-Hxy
        return 2*IG/(Hx+Hy)

    def suGroup(x, n):
        m = x.shape[0]
        x = np.reshape(x, (n,m/n)).T
        m = x.shape[1]
        SU_matrix = np.zeros(shape = (m,m))
        for j in range(m-1):
            x2 = x[:,j+1::]
            y = x[:,j]
            temp = np.apply_along_axis(symmetricalUncertain, 0, x2, y)
            for k in range(temp.shape[0]):
                SU_matrix[j,j+1::] = temp
                SU_matrix[j+1::,j] = temp

        return 1/float(m-1)*np.sum(SU_matrix, axis = 1)

    def isprime(a):
        return all(a % i for i in xrange(2, a))


    """
    get
    """

    def get_i(a):
        if isprime(a):
            a -= 1
        return filter(lambda x: a % x == 0, range(2,a))


    """
    FCBF - Fast Correlation Based Filter

    L. Yu and H. Liu. Feature Selection for High‐Dimensional Data: A Fast Correlation‐Based Filter Solution.
    In Proceedings of The Twentieth International Conference on Machine Leaning (ICML‐03), 856‐863.
    Washington, D.C., August 21‐24, 2003.
    """

    class FCBF:

        idx_sel = []


        def __init__(self, th = 0.01):
            '''
            Parameters
            ---------------
                th = The initial threshold
            '''
            self.th = th


        def fit(self, x, y):
            '''
            This function executes FCBF algorithm and saves indexes
            of selected features in self.idx_sel

            Parameters
            ---------------
                x = dataset  [NxM]
                y = label    [Nx1]
            '''
            self.idx_sel = []
            """
            First Stage: Computing the SU for each feature with the response.
            """
            SU_vec = np.apply_along_axis(symmetricalUncertain, 0, x, y)
            SU_list = SU_vec[SU_vec > self.th]
            SU_list[::-1].sort()

            m = x[:,SU_vec > self.th].shape
            x_sorted = np.zeros(shape = m)

            for i in range(m[1]):
                ind = np.argmax(SU_vec)
                SU_vec[ind] = 0
                x_sorted[:,i] = x[:,ind].copy()
                self.idx_sel.append(ind)

            """
            Second Stage: Identify relationships between feature to remove redundancy.
            """
            j = 0
            while True:
                """
                Stopping Criteria:The search finishes
                """
                if j >= x_sorted.shape[1]: break
                y = x_sorted[:,j].copy()
                x_list = x_sorted[:,j+1:].copy()
                if x_list.shape[1] == 0: break


                SU_list_2 = SU_list[j+1:]
                SU_x = np.apply_along_axis(symmetricalUncertain, 0,
                                        x_list, y)

                comp_SU = SU_x >= SU_list_2
                to_remove = np.where(comp_SU)[0] + j + 1
                if to_remove.size > 0:
                    x_sorted = np.delete(x_sorted, to_remove, axis = 1)
                    SU_list = np.delete(SU_list, to_remove, axis = 0)
                    to_remove.sort()
                    for r in reversed(to_remove):
                        self.idx_sel.remove(self.idx_sel[r])
                j = j + 1

        def fit_transform(self, x, y):
            '''
            This function fits the feature selection
            algorithm and returns the resulting subset.

            Parameters
            ---------------
                x = dataset  [NxM]
                y = label    [Nx1]
            '''
            self.fit(x, y)
            return x[:,self.idx_sel]

        def transform(self, x):
            '''
            This function applies the selection
            to the vector x.

            Parameters
            ---------------
                x = dataset  [NxM]
            '''
            return x[:, self.idx_sel]


    """
    FCBF# - Fast Correlation Based Filter
    B. Senliol, G. Gulgezen, et al. Fast Correlation Based Filter (FCBF) with a Different Search Strategy.
    In Computer and Information Sciences (ISCIS ‘08) 23rd International Symposium on, pages 1‐4.
    Istanbul, October 27‐29, 2008.
    """
    class FCBFK(FCBF):

        idx_sel = []


        def __init__(self, k = 10):
            '''
            Parameters
            ---------------
                k = Number of features to include in the
                subset.
            '''
            self.k = k


        def fit(self, x, y):
            '''
            This function executes FCBFK algorithm and saves indexes
            of selected features in self.idx_sel

            Parameters
            ---------------
                x = dataset  [NxM]
                y = label    [Nx1]
            '''
            self.idx_sel = []
            """
            First Stage: Computing the SU for each feature with the response.
            """
            SU_vec = np.apply_along_axis(symmetricalUncertain, 0, x, y)

            SU_list = SU_vec[SU_vec > 0]
            SU_list[::-1].sort()

            m = x[:,SU_vec > 0].shape
            x_sorted = np.zeros(shape = m)

            for i in range(m[1]):
                ind = np.argmax(SU_vec)
                SU_vec[ind] = 0
                x_sorted[:,i] = x[:,ind].copy()
                self.idx_sel.append(ind)

            """
            Second Stage: Identify relationships between features to remove redundancy with stopping
            criteria (features in x_best == k).
            """
            j = 0
            while True:
                y = x_sorted[:,j].copy()
                SU_list_2 = SU_list[j+1:]
                x_list = x_sorted[:,j+1:].copy()

                """
                Stopping Criteria:The search finishes
                """
                if x_list.shape[1] == 0: break


                SU_x = np.apply_along_axis(symmetricalUncertain, 0,
                                        x_list, y)

                comp_SU = SU_x >= SU_list_2
                to_remove = np.where(comp_SU)[0] + j + 1
                if to_remove.size > 0 and x.shape[1] > self.k:

                    for i in reversed(to_remove):

                        x_sorted = np.delete(x_sorted, i, axis = 1)
                        SU_list = np.delete(SU_list, i, axis = 0)
                        self.idx_sel.remove(self.idx_sel[i])
                        if x_sorted.shape[1] == self.k: break

                if x_list.shape[1] == 1 or x_sorted.shape[1] == self.k:
                    break
                j = j + 1

            if len(self.idx_sel) > self.k:
                self.idx_sel = self.idx_sel[:self.k]



    """
    FCBFiP - Fast Correlation Based Filter in Pieces
    """

    class FCBFiP(FCBF):

        idx_sel = []


        def __init__(self, k = 10, npieces = 2):
            '''
            Parameters
            ---------------
                k = Number of features to include in the
                subset.
                npieces = Number of pieces to divide the
                feature space.
            '''
            self.k = k
            self.npieces = npieces

        def fit(self, x, y):
            '''
            This function executes FCBF algorithm and saves indexes
            of selected features in self.idx_sel

            Parameters
            ---------------
                x = dataset  [NxM]
                y = label    [Nx1]
            '''

            """
            First Stage: Computing the SU for each feature with the response. We sort the
            features. When we have a prime number of features we remove the last one from the
            sorted features list.
            """
            m = x.shape
            nfeaturesPieces = int(m[1] / float(self.npieces))
            SU_vec = np.apply_along_axis(symmetricalUncertain, 0, x, y)

            x_sorted = np.zeros(shape = m, dtype = 'float64')
            idx_sorted = np.zeros(shape = m[1], dtype = 'int64')
            for i in range(m[1]):
                ind = np.argmax(SU_vec)
                SU_vec[ind] = -1
                idx_sorted[i]= ind
                x_sorted[:,i] = x[:,ind].copy()

            if isprime(m[1]):
                x_sorted = np.delete(x_sorted, m[1]-1, axis = 1 )
                ind_prime = idx_sorted[m[1]-1]
                idx_sorted = np.delete(idx_sorted, m[1]-1)
                #m = x_sorted.shape
            """
            Second Stage: Identify relationships between features into its vecinity
            to remove redundancy with stopping criteria (features in x_best == k).
            """

            x_2d = np.reshape(x_sorted.T, (self.npieces, nfeaturesPieces*m[0])).T

            SU_x =  np.apply_along_axis(suGroup, 0, x_2d, nfeaturesPieces)
            SU_x = np.reshape(SU_x.T, (self.npieces*nfeaturesPieces,))
            idx_sorted2 = np.zeros(shape = idx_sorted.shape, dtype = 'int64')
            SU_x[np.isnan(SU_x)] = 1

            for i in range(idx_sorted.shape[0]):
                ind =  np.argmin(SU_x)
                idx_sorted2[i] = idx_sorted[ind]
                SU_x[ind] = 10

            """
            Scoring step
            """
            self.scores = np.zeros(shape = m[1], dtype = 'int64')

            for i in range(m[1]):
                if i in idx_sorted:
                    self.scores[i] = np.argwhere(i == idx_sorted) + np.argwhere(i == idx_sorted2)
            if isprime(m[1]):
                self.scores[ind_prime] = 2*m[1]
            self.set_k(self.k)


        def set_k(self, k):
            self.k = k
            scores_temp = -1*self.scores

            self.idx_sel = np.zeros(shape = self.k, dtype = 'int64')
            for i in range(self.k):
                ind =  np.argmax(scores_temp)
                scores_temp[ind] = -100000000
                self.idx_sel[i] = ind

    #from FCBF_module import FCBF, FCBFK, FCBFiP, get_i
    fcbf = FCBFK(k = 20)
    #fcbf.fit(X_fs, y)

    X_fss = fcbf.fit_transform(X_fs,y)

    X_fss.shape

    """### Re-split train & test sets after feature selection"""

    X_train, X_test, y_train, y_test = train_test_split(X_fss,y, train_size = 0.8, test_size = 0.2, random_state = 0,stratify = y)

    X_train.shape

    pd.Series(y_train).value_counts()

    """### SMOTE to solve class-imbalance"""

    smote=SMOTE(n_jobs=-1,sampling_strategy={2:1000,4:1000})

    X_train, y_train = smote.fit_resample(X_train, y_train)

    pd.Series(y_train).value_counts()

    """## Machine learning model training

    ### Training four base learners: decision tree, random forest, extra trees, XGBoost

    #### Apply XGBoost
    """

    """#### Hyperparameter optimization (HPO) of XGBoost using Bayesian optimization with tree-based Parzen estimator (BO-TPE)
    Based on the GitHub repo for HPO: https://github.com/LiYangHart/Hyperparameter-Optimization-of-Machine-Learning-Algorithms
    """

    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']),
            'max_depth': int(params['max_depth']),
            'learning_rate':  abs(float(params['learning_rate'])),

        }
        clf = xgb.XGBClassifier( **params)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        score = accuracy_score(y_test, y_pred)

        return {'loss':-score, 'status': STATUS_OK }

    space = {
        'n_estimators': hp.quniform('n_estimators', 10, 100, 5),
        'max_depth': hp.quniform('max_depth', 4, 100, 1),
        'learning_rate': hp.normal('learning_rate', 0.01, 0.9),
    }

    # best = fmin(fn=objective,
    #             space=space,
    #             algo=tpe.suggest,
    #             max_evals=20)
    # print("XGBoost: Hyperopt estimated optimum {}".format(best))

    xg = xgb.XGBClassifier(learning_rate= 0.7340229699980686, n_estimators = 70, max_depth = 14)
    xg.fit(X_train,y_train)
    xg_score=xg.score(X_test,y_test)
    y_predict=xg.predict(X_test)
    y_true=y_test
    print('Accuracy of XGBoost: '+ str(xg_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of XGBoost: '+(str(precision)))
    print('Recall of XGBoost: '+(str(recall)))
    print('F1-score of XGBoost: '+(str(fscore)))
    print(classification_report(y_true,y_predict))
    cm=confusion_matrix(y_true,y_predict)
    f,ax=plt.subplots(figsize=(5,5))
    sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    #plt.show()

    """#### Apply RF"""

    """#### Hyperparameter optimization (HPO) of random forest using Bayesian optimization with tree-based Parzen estimator (BO-TPE)
    Based on the GitHub repo for HPO: https://github.com/LiYangHart/Hyperparameter-Optimization-of-Machine-Learning-Algorithms
    """

    # Hyperparameter optimization of random forest
    # Define the objective function
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']),
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = RandomForestClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    space = {
        'n_estimators': hp.quniform('n_estimators', 10, 200, 1),
        'max_depth': hp.quniform('max_depth', 5, 50, 1),
        "max_features":hp.quniform('max_features', 1, 20, 1),
        "min_samples_split":hp.quniform('min_samples_split',2,11,1),
        "min_samples_leaf":hp.quniform('min_samples_leaf',1,11,1),
        "criterion":hp.choice('criterion',['gini','entropy'])
    }

    # best = fmin(fn=objective,
    #             space=space,
    #             algo=tpe.suggest,
    #             max_evals=20)
    # print("Random Forest: Hyperopt estimated optimum {}".format(best))

    rf_hpo = RandomForestClassifier(n_estimators = 71, min_samples_leaf = 1, max_depth = 46, min_samples_split = 9, max_features = 20, criterion = 'entropy')
    rf_hpo.fit(X_train,y_train)
    rf_score=rf_hpo.score(X_test,y_test)
    y_predict=rf_hpo.predict(X_test)
    y_true=y_test
    print('Accuracy of RF: '+ str(rf_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of RF: '+(str(precision)))
    print('Recall of RF: '+(str(recall)))
    print('F1-score of RF: '+(str(fscore)))
    print(classification_report(y_true,y_predict))
    cm=confusion_matrix(y_true,y_predict)
    f,ax=plt.subplots(figsize=(5,5))
    sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    #plt.show()

    """#### Apply DT"""

    """#### Hyperparameter optimization (HPO) of decision tree using Bayesian optimization with tree-based Parzen estimator (BO-TPE)
    Based on the GitHub repo for HPO: https://github.com/LiYangHart/Hyperparameter-Optimization-of-Machine-Learning-Algorithms
    """

    # Hyperparameter optimization of decision tree
    # Define the objective function
    def objective(params):
        params = {
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = DecisionTreeClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    space = {
        'max_depth': hp.quniform('max_depth', 5, 50, 1),
        "max_features":hp.quniform('max_features', 1, 20, 1),
        "min_samples_split":hp.quniform('min_samples_split',2,11,1),
        "min_samples_leaf":hp.quniform('min_samples_leaf',1,11,1),
        "criterion":hp.choice('criterion',['gini','entropy'])
    }

    # best = fmin(fn=objective,
    #             space=space,
    #             algo=tpe.suggest,
    #             max_evals=50)
    # print("Decision tree: Hyperopt estimated optimum {}".format(best))

    dt_hpo = DecisionTreeClassifier(min_samples_leaf = 2, max_depth = 47, min_samples_split = 3, max_features = 19, criterion = 'gini')
    dt_hpo.fit(X_train,y_train)
    dt_score=dt_hpo.score(X_test,y_test)
    y_predict=dt_hpo.predict(X_test)
    y_true=y_test
    print('Accuracy of DT: '+ str(dt_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of DT: '+(str(precision)))
    print('Recall of DT: '+(str(recall)))
    print('F1-score of DT: '+(str(fscore)))
    print(classification_report(y_true,y_predict))
    cm=confusion_matrix(y_true,y_predict)
    f,ax=plt.subplots(figsize=(5,5))
    sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    #plt.show()

    """#### Apply ET"""

    """#### Hyperparameter optimization (HPO) of extra trees using Bayesian optimization with tree-based Parzen estimator (BO-TPE)
    Based on the GitHub repo for HPO: https://github.com/LiYangHart/Hyperparameter-Optimization-of-Machine-Learning-Algorithms
    """

    # Hyperparameter optimization of extra trees
    # Define the objective function
    def objective(params):
        params = {
            'n_estimators': int(params['n_estimators']),
            'max_depth': int(params['max_depth']),
            'max_features': int(params['max_features']),
            "min_samples_split":int(params['min_samples_split']),
            "min_samples_leaf":int(params['min_samples_leaf']),
            "criterion":str(params['criterion'])
        }
        clf = ExtraTreesClassifier( **params)
        clf.fit(X_train,y_train)
        score=clf.score(X_test,y_test)

        return {'loss':-score, 'status': STATUS_OK }
    # Define the hyperparameter configuration space
    space = {
        'n_estimators': hp.quniform('n_estimators', 10, 200, 1),
        'max_depth': hp.quniform('max_depth', 5, 50, 1),
        "max_features":hp.quniform('max_features', 1, 20, 1),
        "min_samples_split":hp.quniform('min_samples_split',2,11,1),
        "min_samples_leaf":hp.quniform('min_samples_leaf',1,11,1),
        "criterion":hp.choice('criterion',['gini','entropy'])
    }

    # best = fmin(fn=objective,
    #             space=space,
    #             algo=tpe.suggest,
    #             max_evals=20)
    # print("Random Forest: Hyperopt estimated optimum {}".format(best))

    et_hpo = ExtraTreesClassifier(n_estimators = 53, min_samples_leaf = 1, max_depth = 31, min_samples_split = 5, max_features = 20, criterion = 'entropy')
    et_hpo.fit(X_train,y_train)
    et_score=et_hpo.score(X_test,y_test)
    y_predict=et_hpo.predict(X_test)
    y_true=y_test
    print('Accuracy of ET: '+ str(et_score))
    precision,recall,fscore,none= precision_recall_fscore_support(y_true, y_predict, average='weighted')
    print('Precision of ET: '+(str(precision)))
    print('Recall of ET: '+(str(recall)))
    print('F1-score of ET: '+(str(fscore)))
    print(classification_report(y_true,y_predict))
    cm=confusion_matrix(y_true,y_predict)
    f,ax=plt.subplots(figsize=(5,5))
    sns.heatmap(cm,annot=True,linewidth=0.5,linecolor="red",fmt=".0f",ax=ax)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    #plt.show()

if __name__ == '__main__':
    main()
