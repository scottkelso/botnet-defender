import glob, os
from joblib import load
from training.dataLoader import preprocess_test_data


def evaluate(file, filemove=True):
    if filemove:
        print("Moving " + file + " for processing...")
        os.rename(traffic_dir + "capture/" + file, traffic_dir + "processed/" + file)
        filepath = traffic_dir + "processed/" + file
    else:
        filepath = traffic_dir + "capture/" + file

    print("Preprocessing " + file + " for ML...")
    data = preprocess_test_data(filepath)

    print("Predicting " + file + " for botnet traffic...")
    classifications = m.predict(data)
    probabilities = m.predict_proba(data)

    for i, prediction in enumerate(classifications):
        print("[{0}] {1} with {2:.3f} probability".format(i, prediction, max(probabilities[i])))


m = load('../training/svm.joblib')

traffic_dir = "../../traffic/"
os.chdir("../../traffic/capture/")
queue = []
for file in glob.glob("*.csv"):
    queue.append(file)

for testfile in queue:
    evaluate(testfile, filemove=False)
