# Machine Learning Tuning
DATA / FEATURE SELECTION
* Run racluster on the datasets
* Compare OrdinalEncoder vs OneHotEncoder (OneHotEncoder should be better)
* Ridge Regularisation vs. Lasso
* Include Sport / Dport string labelled records but make null value

KNN
* `k` and `distance` in KNN

SVM
* https://scikit-learn.org/stable/auto_examples/svm/plot_svm_scale_c.html


# Machine Learning Tuning
| Algorithm   | Data Size     | Accuracy      | Train Time   | Test Time    |
|-------------|:-------------:|:-------------:|-------------:|-------------:|
| KNN         | 500,000       | 0.996         | 720          | 25           |
| SVM         | 500,000       | 0.579         | 4084         | 27           | 
| Ran Forest  | 500,000       | 0.999         | 20           | < 1          |


# Helpful Articles
* https://elitedatascience.com/imbalanced-classes
* https://docs.python.org/3/library/configparser.html
* https://www.youtube.com/watch?v=N5vscPTWKOk&t=206s
* https://stats.stackexchange.com/questions/267012/difference-between-preprocessing-train-and-test-set-before-and-after-splitting