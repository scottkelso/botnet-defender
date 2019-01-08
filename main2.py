from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

import pandas as pd
import numpy as np

data = pd.read_csv('data/OS_Scan.csv', sep=';')
print("Hello World!")
print(data.head())

labels = data[['category']]
data = data.drop(
    ['subcategory', 'category', 'attack', 'record', 'dco', 'sco', 'doui', 'soui', 'dmac', 'smac', 'seq'], axis=1)

# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)

clf = svm.SVC(gamma='scale', probability=True, max_iter=1000)
clf.fit(data, labels)

# Evaulate the model on the augmented test data
means = X_train.mean(axis=0)
stds = X_train.std(axis=0)

X_test_input = X_test - np.expand_dims(means, 0)
X_test_input /= np.expand_dims(stds, 0)

predictions = clf.predict(X_test)
print("F1 score:", f1_score(X_test, predictions, average='weighted'))
