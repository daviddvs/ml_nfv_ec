import pandas as pd
from pandas import DataFrame
import numpy as np
import pylab
import scipy.stats as stats
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import random
from sklearn import datasets, linear_model, tree, cluster, metrics, decomposition
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import pydotplus
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
import pickle
import datetime

#%matplotlib inline
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
        timestamp = datetime.datetime.now().timestamp()
        for i in range(1,N+1):
            p_test = model.predict(x_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = N*len(x_test)
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
        else:
            return ml.regressor(upfile,N)


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
        timestamp = datetime.datetime.now().timestamp()
        for i in range(1,N+1):
            p_test = model.predict(x_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        elem = N*len(x_test)
        print('Prediction finished in {0:.2f} ms for {1} elements'.format(prediction_time_ms, elem))
        return [prediction_time_ms, elem] #return an array for the REST API


    def clustering(): # The goal is to recognise handwritten digits
        
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
        timestamp = datetime.datetime.now().timestamp()
        y_pred = clf.predict(X_test)
        now = datetime.datetime.now().timestamp()
        prediction_time_ms = (float(now) - float(timestamp))*1000
        print('Prediction finished in {0:.2f} ms'.format(prediction_time_ms))
        #for i in range(10):
            #print_cluster(images_test, y_pred, i)
        #plt.show()

        '''
        # Evaluate the Model
        print('Adjusted rand score: {0:2}'.format(metrics.adjusted_rand_score(y_test, y_pred)))
        print('Confussion Matrix:\n',metrics.confusion_matrix(y_test, y_pred))
        '''
        
        '''
        # Reduce to 2 components
        pca = decomposition.PCA(n_components=2).fit(X_train)
        reduced_X_train = pca.transform(X_train)
        # Step size of the mesh. 
        h = .01     
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        x_min, x_max = reduced_X_train[:, 0].min() + 1, reduced_X_train[:, 0].max() - 1
        y_min, y_max = reduced_X_train[:, 1].min() + 1, reduced_X_train[:, 1].max() - 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
            np.arange(y_min, y_max, h))
        kmeans = cluster.KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
        kmeans.fit(reduced_X_train)
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        '''

        '''
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.clf()
        plt.figure(1)
        plt.clf()
        plt.imshow(Z, interpolation='nearest', extent=(xx.min(), xx.max(), yy.min(), yy.max()), 
            cmap=plt.cm.Paired, aspect='auto', origin='lower')
        plt.plot(reduced_X_train[:, 0], reduced_X_train[:, 1], 'k.', 
            markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],marker='.', 
            s=169, linewidths=3, color='w', zorder=10)
        plt.title('K-means clustering on the digits dataset (PCA reduced data)\nCentroids are marked with white dots')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.show()
        '''

#wines_dataset()
#pred_time = machine_learning.rocksMines_dataset()
#clustering()
#machine_learning.predict()
