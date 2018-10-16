import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import ensemble
from sklearn import datasets

dataset = pd.read_table('dist_11x8_train_part.txt', header = -1, sep = '\t')
dataset = dataset.astype(np.float32)
dataset = np.array(dataset)
X = dataset[:, :-1]
y = dataset.T[-1]
for i in range(len(y)):
    y[i] = y[i]-1
    
X_train = X
y_train = y

original_params = {'n_estimators': 1000, 'max_leaf_nodes': 4, 'max_depth': None, 'random_state': 2,
                   'min_samples_split': 5}
setting = {'learning_rate': 0.1, 'subsample': 0.5}
params = dict(original_params)
params.update(setting)

clf = ensemble.GradientBoostingClassifier(**params)
clf.fit(X_train, y_train)

data_test = pd.read_table('dist_11x8_test.txt', header = -1, sep = '\t')
data_test = data_test.astype(np.float32)
data_test = np.array(data_test)
X_test = data_test[:, :-1]
Y_test = clf.predict(X_test)
print(Y_test)

dataset = pd.read_table('dist_11x8_train_cheg.txt', header = -1, sep = '\t')
dataset = dataset.astype(np.float32)
dataset = np.array(dataset)
X = dataset[:, :-1]
y = dataset.T[-1]
for i in range(len(y)):
    y[i] = y[i]-1
X_train = X
y_train = y

clf = ensemble.GradientBoostingClassifier(**params)
clf.fit(X_train, y_train)

data_test = pd.read_table('dist_11x8_test.txt', header = -1, sep = '\t')
data_test = data_test.astype(np.float32)
data_test = np.array(data_test)
X_test = data_test[:, :-1]
Y_test = clf.predict(X_test)
print(Y_test)

