import pandas as pd
import numpy as np
from sklearn import cluster
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
import pickle
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import sys, os

class machine_learning:
    
    def __init__(self):
        self.model_dir="models"
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            print("INFO: Directory "+self.model_dir+" created.")
    
    def update_model(self,filename):

        # Update model in the backend
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        hostfile = self.model_dir+'/hosts.p'
        hosts = pickle.load(open(hostfile, 'rb'))
        for h in hosts:
            ssh.connect(h["IP"], username=h["username"], password=h["password"], allow_agent=False)
            # SCPCLient takes a paramiko transport as an argument
            scp = SCPClient(ssh.get_transport())
            # Uploading file to remote path
            rem_path='~/ml_nfv_ec/backend/models'
            scp.put(filename, remote_path=rem_path)
            scp.close()
            print('Model updated in host: '+h["IP"])


    def regressor(self): # DecisionTreeRegressor

        # Load dataset
        url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
        w_df = pd.read_csv(url,header=0,sep=';')

        # Divide dataset into training and test samples
        train, test = train_test_split(w_df, test_size = 0.3)
        x_train = train.iloc[0:,0:11]
        y_train = train[['quality']]
        x_test = test.iloc[0:,0:11]
        y_test = test[['quality']]

        # Decision Tree Model: We see that the best depth is 3 - 4
        model = DecisionTreeRegressor(max_depth=3)
        model.fit(x_train,y_train)

        # Save the model to disk
        filename = self.model_dir+'/decisionTreeRegressor_model.p'
        pickle.dump(model, open(filename, 'wb'))
        print('Model DecissionTreeRegressor saved into -> ./'+filename)

        # Update model
        self.update_model(filename)


    def classifier(self): # DecisionTreeClassifier

        # Load dataser
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data"
        df = pd.read_csv(url,header=None)

        # Divide dataset into training and test samples     
        df[60]=np.where(df[60]=='R',0,1)
        #print(df.describe())
        train, test = train_test_split(df, test_size = 0.3)
        x_train = train.iloc[0:,0:60]
        y_train = train[[60]]
        x_test = test.iloc[0:,0:60]
        y_test = test[[60]]

        # Decision Tree Model
        model = DecisionTreeClassifier(max_depth=3,criterion='entropy')
        model.fit(x_train,y_train)
        
        # Save the model to disk
        filename = self.model_dir+'/decisionTreeClassifier_model.p'
        pickle.dump(model, open(filename, 'wb'))
        print('Model DecissionTreeClassifier saved into -> ./'+filename)

        # Update model
        self.update_model(filename)
        

    def clustering(self): # The goal is to recognise handwritten digits
        
        #Load data
        digits = load_digits()
        data = scale(digits.data)

        # Training and testing samples
        X_train, X_test, y_train, y_test, images_train, images_test = train_test_split(
                data, digits.target, digits.images, test_size=0.25, random_state=42)
        
        n_samples, n_features = X_train.shape
        n_digits = len(np.unique(y_train))
        labels = y_train

        # Clustering-KMeans Model
        clf = cluster.KMeans(init='k-means++',n_clusters=10, random_state=42)
        clf.fit(X_train)

        # Save the model to disk
        filename = self.model_dir+'/KMeansCluster_model.p'
        pickle.dump(clf, open(filename, 'wb'))
        print('Model KMeansCluster saved into -> ./'+filename)

        # Update model
        self.update_model(filename)
