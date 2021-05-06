# Download data here
#https://medium.com/@jamesstradling/unsupervised-machine-learning-with-one-class-support-vector-machines-129579a49d1d

import numpy as np
import pandas as pd
from sklearn import utils
import matplotlib
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.externals import joblib

# import the CSV
data = pd.read_csv('~/Downloads/kddcup.data_10_percent.csv', low_memory=False)

# normalise the data - this leads to better accuracy and reduces
# numerical instability in the SVM implementation
data["duration"] = np.log((data["duration"] + 0.1).astype(float))
data["src_bytes"] = np.log((data["src_bytes"] + 0.1).astype(float))
data["dst_bytes"] = np.log((data["dst_bytes"] + 0.1).astype(float))

# we're using a one-class SVM, so we need.. a single class. the
# dataset 'label' column contains multiple different categories of
# attacks, so to make use of this data in a one-class system we need
# to convert the attacks into class 1 (normal) and class -1 (attack)
data.loc[data['label'] == "normal.", "attack"] = 1
data.loc[data['label'] != "normal.", "attack"] = -1

# grab out the attack value as the target for training and testing.
# since we're only selecting a single column from the `data`
# dataframe, we'll just get a series, not a new dataframe
target = data['attack']

# find the proportion of outliers we expect (aka where `attack ==
# -1`). because target is a series, we just compare against itself
# rather than a column.
outliers = target[target == -1]
print("outliers.shape", outliers.shape)
print("outlier fraction", outliers.shape[0]/target.shape[0])

# drop label columns from the dataframe. we're doing this so we can # do unsupervised training with unlabelled data. we've already
# copied the label out into the target series so we can compare
# against it later.
data.drop(["label", "attack"], axis=1, inplace=True)

# check the shape for sanity checking.
data.shape

train_data, test_data, train_target, test_target = train_test_split(data, target, train_size = 0.8)
train_data.shape

# set nu (which should be the proportion of outliers in our dataset)
nu = outliers.shape[0] / target.shape[0]
print("nu", nu)
model = svm.OneClassSVM(nu=nu, kernel='rbf', gamma=0.00005)
model.fit(train_data)

preds = model.predict(train_data)
targs = train_target print("accuracy: ", metrics.accuracy_score(targs, preds))
print("precision: ", metrics.precision_score(targs, preds))
print("recall: ", metrics.recall_score(targs, preds))
print("f1: ", metrics.f1_score(targs, preds))
print("area under curve (auc): ", metrics.roc_auc_score(targs, preds))

preds = model.predict(test_data)
targs = test_target print("accuracy: ", metrics.accuracy_score(targs, preds))
print("precision: ", metrics.precision_score(targs, preds))
print("recall: ", metrics.recall_score(targs, preds))
print("f1: ", metrics.f1_score(targs, preds))
print("area under curve (auc): ", metrics.roc_auc_score(targs, preds))

data = pd.read_json(some_json)
model.predict(data)

outputfile = 'oneclass_v1.model'
joblib.dump(model, outputfile, compress=9)

model = joblib.load('oneclass_v1.model')
# then predict with model.predict(..)
