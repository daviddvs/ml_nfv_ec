import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
import pickle
import datetime

class machine_learning:

    def confusion_matrix(predicted, actual, threshold):
        if len(predicted) != len(actual): return -1
        tp = 0.0
        fp = 0.0
        tn = 0.0
        fn = 0.0
        for i in range(len(actual)):
            if actual[i] > 0.5: #labels that are 1.0  (positive examples)
                if predicted[i] > threshold:
                    tp += 1.0 #correctly predicted positive
                else:
                    fn += 1.0 #incorrectly predicted negative
            else:              #labels that are 0.0 (negative examples)
                if predicted[i] < threshold:
                    tn += 1.0 #correctly predicted negative
                else:
                    fp += 1.0 #incorrectly predicted positive
        rtn = [tp, fn, fp, tn]
        
        return rtn


    def regressor(self, uof, N=1): # Wines dataset, uof = url or file, DecisionTreeRegressor

        # Load dataset
        w_df = pd.read_csv(uof,header=0,sep=';')

        # Divide dataset into training and test samples
        train, test = train_test_split(w_df, test_size = 0.3)
        x_train = train.iloc[0:,0:11]
        y_train = train[['quality']]
        x_test = test.iloc[0:,0:11]
        y_test = test[['quality']]

        # Load the model from disk
        filename = 'models/decisionTreeRegressor_model.p'
        model = pickle.load(open(filename, 'rb'))

        # Prediction
        for i in range(1,N+1):
            x_test = np.concatenate((x_test,x_test), axis=0)
        timestamp = datetime.datetime.now().timestamp()    
        p_test = model.predict(x_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(x_test)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem] #return an array for the REST API


    def predict(N=1,typ=0):
        
        # Load dataset
        url_classifier="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
        url_regressor="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

        # Start prediction
        print("Prediction type: "+str(typ))
        ml=machine_learning()
        if(typ==0):
            return ml.classifier(url_classifier,N)
        else:
            return ml.regressor(url_regressor,N)

    def predict_data(N=1, upfile=None, typ=0):
        
        # Check file (can be deleted)
        if(upfile != None):
            print("File received!")
        else:
            print("No file received!")
        
        # Start prediction
        ml=machine_learning()
        if(typ==0):
            return ml.classifier(upfile,N)
        elif(typ==1):
            return ml.regressor(upfile,N)
        else:
            return ml.clustering(N)


    def classifier(self, uof, N=1): # Rocks/Mines dataset, uof= url or file, DecisionTreeClassifier
       
        # Load dataset
        df = pd.read_csv(uof,header=None)

        # Divide dataset into training and test samples     
        df[60]=np.where(df[60]=='R',0,1)
        #print(df.describe())
        train, test = train_test_split(df, test_size = 0.3)
        x_train = train.iloc[0:,0:60]
        y_train = train[[60]]
        x_test = test.iloc[0:,0:60]
        y_test = test[[60]]

        # Load the model from disk
        filename = 'models/decisionTreeClassifier_model.p'
        model = pickle.load(open(filename, 'rb'))
        
        # Prediction and ROC Curve
        for i in range(1,N+1):
            x_test = np.concatenate((x_test,x_test), axis=0)
        timestamp = datetime.datetime.now().timestamp()
        p_test = model.predict(x_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(x_test)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem] #return an array for the REST API


    def clustering(self, N=1): # The goal is to recognise handwritten digits
        
        #Load data
        digits = load_digits()
        data = scale(digits.data)

        # Show data
        #print_digits(digits.images, digits.target, max_n=10)
        #plt.show()

        # Training and testing samples
        X_train, X_test, y_train, y_test, images_train, images_test = train_test_split(
                data, digits.target, digits.images, test_size=0.25, random_state=42)
        
        n_samples, n_features = X_train.shape
        n_digits = len(np.unique(y_train))
        labels = y_train

        # Load the model from disk
        filename = 'models/KMeansCluster_model.p'
        clf = pickle.load(open(filename, 'rb'))

        # Use test sample to generate predictions
        for i in range(1,N+1):
            X_test = np.concatenate((X_test,X_test), axis=0)
        timestamp = datetime.datetime.now().timestamp()
        y_pred = clf.predict(X_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(X_test)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem]
        #for i in range(10):
            #print_cluster(images_test, y_pred, i)
        #plt.show()

#machine_learning.clustering()
#url_classifier="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
#ml = machine_learning()
#ml.classifier(uof=url_classifier, N=10)

