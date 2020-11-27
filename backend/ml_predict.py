import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn import cluster
import pickle
import datetime

class machine_learning:

    def regressor(self, uof, N=1): # Wines dataset, uof = url or file, DecisionTreeRegressor

        # Load the model from disk
        filename = 'models/decisionTreeRegressor_model.p'
        model = pickle.load(open(filename, 'rb'))

        # Get content (reshape to N rows and 11 cols)
        content = np.array(uof['upfile']).reshape((N,11))
     
        # Predict
        timestamp = datetime.datetime.now().timestamp()    
        p_test = model.predict(content)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(content)
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
            return ml.clustering(upfile,N)


    def classifier(self, uof, N=1): # Rocks/Mines dataset, uof= url or file, DecisionTreeClassifier
       
        # Load the model from disk
        filename = 'models/decisionTreeClassifier_model.p'
        model = pickle.load(open(filename, 'rb'))
        
        # Get content (reshape to N rows and 60 cols)
        content = np.array(uof['upfile']).reshape((N,60))

        # Predict
        timestamp = datetime.datetime.now().timestamp()
        p_test = model.predict(content)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(content)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem] #return an array for the REST API


    def clustering(self, uof, N=1): # The goal is to recognise handwritten digits

        # Load the model from disk
        filename = 'models/KMeansCluster_model.p'
        clf = pickle.load(open(filename, 'rb'))

        # Get content (reshape to N rows and 64 cols)
        content = np.array(uof['upfile']).reshape((N,64))

        # Predict
        timestamp = datetime.datetime.now().timestamp()
        y_pred = clf.predict(content)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = len(content)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem]