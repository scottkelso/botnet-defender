import pandas as pd
import numpy as np

from utils.reader import sessionizer
from utils.pcap_utils import get_source
from utils.featurizer import extract_features


def read_scan_csv():
    data = pd.read_csv('data/OS_Scan.csv', sep=';')
    print("Hello World!")
    print(data.head())

    labels = data[['category']]
    data = data.drop(
        ['subcategory', 'category', 'attack', 'record', 'dco', 'sco', 'doui', 'soui', 'dmac', 'smac', 'seq'], axis=1)


# def read_pcap(filename):

X = []
y = []
assigned_labels = []

# Device Label
label = 'Unknown'
if label not in assigned_labels:
    assigned_labels.append(label)

print("Launching sessionizer...")

# Bin the sessions with the specified time window
binned_sessions = sessionizer("data/IoT_Dataset_OSScan__00001_20180521140502.pcap")

print("Getting Sources...")

# Get the capture source from the binned sessions
capture_source = get_source(binned_sessions)

print("Extracting Features...")

# For each of the session bins, compute the  full feature vectors
for session_dict in binned_sessions:
    features, _, _ = extract_features(
        session_dict,
        capture_source=capture_source
    )

    # Store the feature vector and the labels
    X.append(features)
    # y.append(assigned_labels.index(label))

    # return np.stack(X), np.stack(y)

np.stack(X)
# X_all, y_all = read_pcap("data/201608041359-sliced1")
