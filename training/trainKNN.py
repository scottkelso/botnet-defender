from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from joblib import dump
from training.dataLoader import get_data
import time

X, y, _ = get_data()

# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("Training KNN Model...")
# clf = neighbors.KNeighborsClassifier(n_neighbors=3)
clf = neighbors.KNeighborsClassifier()

t0 = time.time()
clf.fit(X_train, y_train)
t1 = time.time()
total = t1-t0
print("Training Finished in "+str(total)+" seconds!")

# # # Evaulate the model on the augmented test data
# # means = X_train.mean(axis=0)
# # stds = X_train.std(axis=0)
# #
# # X_test_input = X_test - np.expand_dims(means, 0)
# # X_test_input /= np.expand_dims(stds, 0)
# print("F1 score:", f1_score(X_test, predictions, average='weighted'))

print("Calculating Simple Accuracy...")
t0 = time.time()
predictions = clf.predict(X_test)
t1 = time.time()
total = t1-t0
print("Predicting Finished in "+str(total)+" seconds!")
print("Accuracy:", accuracy_score(y_test, predictions))

# dump(clf, 'knn.joblib')
