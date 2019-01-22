from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from joblib import dump

import pandas as pd
import numpy as np

import socket
import struct


def ip2int(addr):
    address_int = 'DROP'
    try:
        address_int = struct.unpack("!I", socket.inet_aton(addr))[0]
    except OSError:
        print('Unable to parse ip address ' + addr)
    return address_int


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def read_csv(path):
    print("Reading CSV...")
    all_data = pd.read_csv(path, sep=';')
    rows = all_data.drop(
        ['subcategory',
         'attack',
         'record',
         'dco',
         'sco',
         'doui',
         'soui',
         'dmac',
         'smac',
         'seq',
         'flgs'], axis=1
    )

    return rows


def preprocessing(df):
    print("Preprocessing Data...")
    # Drop all ipv6 and icmp packets
    # df = df[~df.proto.str.contains("ipv6")]
    # df = df[~df.proto.str.contains("icmp")]
    # df = df.reset_index(drop=True)

    # # TODO(jk): Make work for none tcp packets
    # Select only tcp packets
    df = df[df['proto'].str.contains("tcp")]
    df = df.drop(['proto'], axis=1)
    df = df.reset_index(drop=True)

    # Convert ip addresses to int
    ip_address_labels = ['saddr', 'daddr', 'srcid']
    # TODO(jk): For loop
    df['saddr'] = df['saddr'].apply(ip2int)
    df['daddr'] = df['daddr'].apply(ip2int)
    df['srcid'] = df['srcid'].apply(ip2int)

    # df.proto = df.proto.astype('category').cat.codes
    df.dir = df.dir.astype('category').cat.codes
    df.state = df.state.astype('category').cat.codes

    return df


data = read_csv('data/OS_Scan.csv')
data = preprocessing(data)

X = data.drop(columns=['category'])
y = data['category']
print(data['category'].value_counts())


# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("Training Model...")
clf = svm.SVC(gamma='scale', probability=True, max_iter=1000)
clf.fit(X_train, y_train)

# # Evaulate the model on the augmented test data
# means = X_train.mean(axis=0)
# stds = X_train.std(axis=0)
#
# X_test_input = X_test - np.expand_dims(means, 0)
# X_test_input /= np.expand_dims(stds, 0)

predictions = clf.predict(X_test)
# print("F1 score:", f1_score(X_test, predictions, average='weighted'))

print("Accuracy:", accuracy_score(y_test, predictions))

dump(clf, 'filename.joblib')
