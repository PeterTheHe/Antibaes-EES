print(__doc__)

import os
import glob
import numpy as np
from sklearn import svm

X_train = []
X_test = []
X_negatives = []

#Load examples
directory = input('Where are the training examples stored? ')

for filename in glob.glob(os.path.join(directory, '*.txt')):
    X_train.append(np.loadtxt(filename))
print ("Bare Loaded")
    
#Load Positive Test Set
directory = input('Where are the POSITIVE testing examples stored? ')

for filename in glob.glob(os.path.join(directory, '*.txt')):
    X_test.append(np.loadtxt(filename))
print ("Bare Loaded")

#Load Negative Test Set
directory = input('Where are the NEGATIVE testing examples stored? ')

for filename in glob.glob(os.path.join(directory, '*.txt')):
    X_negatives.append(np.loadtxt(filename))
print ("Bare Loaded")

#Train the SVM
clf = svm.OneClassSVM(nu=0.25, kernel="rbf", gamma=0.1)
clf.fit(X_train)

#Predict things
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
y_pred_negatives = clf.predict(X_negatives)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
n_error_negatives = y_pred_negatives[y_pred_negatives == 1].size
print ("Training Error: " + str(n_error_train))
print ("Positive Testing Error: " + str(n_error_test))
print ("Negative Testing Error: " + str(n_error_negatives))