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

#%matplotlib inline

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


def wines_dataset():

    # Load dataset
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    w_df = pd.read_csv(url,header=0,sep=';')

    # Divide dataset into training and test samples
    train, test = train_test_split(w_df, test_size = 0.3)
    x_train = train.iloc[0:,0:11]
    y_train = train[['quality']]
    x_test = test.iloc[0:,0:11]
    y_test = test[['quality']]

    # Use all data for cross validation
    x_data = w_df.iloc[0:,0:11]
    y_data = w_df[['quality']]

    # Decision Tree Model
    model = DecisionTreeRegressor(max_depth=3)
    model.fit(x_train,y_train)

    # Classifiers
    print('Train R-Square: ',model.score(x_train,y_train))
    print('Test R-Square: ',model.score(x_test,y_test))

    # Cross validation
    crossvalidation = KFold(n_splits=5,shuffle=True, random_state=1)
    for depth in range(1,10):
        model = tree.DecisionTreeRegressor(
        max_depth=depth, random_state=0)
        if model.fit(x_data,y_data).tree_.max_depth < depth:
            break
        score = np.mean(cross_val_score(model, x_data, y_data,scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print ('Depth: %i Accuracy: %.3f' % (depth,score))

    # We see that the best depth is 3 - 4
    model = DecisionTreeRegressor(max_depth=3)
    model.fit(x_train,y_train)

    # View the tree (the tree will be saved to wines2.pdf in your current directory)
    feature_names = [key for key in w_df.iloc[0:,0:11]]
    dot_data = tree.export_graphviz(model,out_file=None,feature_names=feature_names) 
    graph = pydotplus.graph_from_dot_data(dot_data) 
    #graph.write_pdf("wines2.pdf") 


def rocksMines_dataset():

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
    
    # save the model to disk
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    print('Model saved')


def print_digits(images,y,max_n=10):

    # set up the figure size in inches
    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1,
            hspace=.05, wspace=.5)
    i = 0
    while i <max_n and i <images.shape[0]:
        # plot the images in a matrix of 20x20
        p = fig.add_subplot(20, 20, i + 1, xticks=[],
                yticks=[])
        p.imshow(images[i], cmap=plt.cm.bone)
        # label the image with the target value
        p.text(0, 14, str(y[i]))
        i = i + 1


def print_cluster(images, y_pred, cluster_number):
    images = images[y_pred==cluster_number]
    y_pred = y_pred[y_pred==cluster_number]
    print_digits(images, y_pred,max_n=15)
    

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

    # Clustering-KMeans Model
    clf = cluster.KMeans(init='k-means++',n_clusters=10, random_state=42)
    clf.fit(X_train)

    # Show clusters
    #print_digits(images_train,clf.labels_,max_n=20)
    #plt.show()

    # Use test sample to generate predictions
    y_pred = clf.predict(X_test)
    #for i in range(10):
        #print_cluster(images_test, y_pred, i)
    #plt.show()

    # Evaluate the Model
    print('Adjusted rand score: {0:2}'.format(metrics.adjusted_rand_score(y_test, y_pred)))
    print('Confussion Matrix:\n',metrics.confusion_matrix(y_test, y_pred))    
    
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

#wines_dataset()
rocksMines_dataset()
#clustering()

