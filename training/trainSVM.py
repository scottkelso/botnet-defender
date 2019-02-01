from sklearn import svm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score, accuracy_score
from joblib import dump
from training.dataLoader import get_data

X, y = get_data()

# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("Training SVC Model...")
clf = svm.SVC(gamma='scale', probability=True, max_iter=1000)

scores = cross_val_score(clf, X, y, cv=5)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# clf.fit(X_train, y_train)
#
# # # Evaulate the model on the augmented test data
# # means = X_train.mean(axis=0)
# # stds = X_train.std(axis=0)
# #
# # X_test_input = X_test - np.expand_dims(means, 0)
# # X_test_input /= np.expand_dims(stds, 0)
#
# predictions = clf.predict(X_test)
# # print("F1 score:", f1_score(X_test, predictions, average='weighted'))
#
# print("Accuracy:", accuracy_score(y_test, predictions))

dump(clf, 'svm.joblib')
