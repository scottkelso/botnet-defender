from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

import pandas as pd
import numpy as np

import socket
import struct


def ip2int(addr):
    address_int = ''
    try:
        address_int = struct.unpack("!I", socket.inet_aton(addr))[0]
    except OSError:
        print('Unable to parse ip address ' + addr)
    return address_int


def can_ip2int(addr):
    address_int = False
    try:
        address_int = struct.unpack("!I", socket.inet_aton(addr))[0]
        address_int = True
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
         'seq'], axis=1
    )

    return rows, labels


def preprocessing(df):
    # Drop all ipv6 addressed packets
    df = df.drop(df[df.proto == 'ipv6-icmp'].index)

    # Convert ip addresses to int
    ip_address_labels = ['saddr', 'daddr', 'srcid']
    # TODO(jk): For loop
    df['saddr'] = df['saddr'].apply(lambda x: ip2int(x))
    df['daddr'] = df['daddr'].apply(lambda x: ip2int(x))
    df['srcid'] = df['srcid'].apply(lambda x: ip2int(x))

    return df


data, labels = read_csv('data/OS_Scan.csv')

# # https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
# data[data['saddr'].map(can_ip2int)]

data = preprocessing(data)

# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)

clf = svm.SVC(gamma='scale', probability=True, max_iter=1000)
# clf.fit(data, labels)
#
# # Evaulate the model on the augmented test data
# means = X_train.mean(axis=0)
# stds = X_train.std(axis=0)
#
# X_test_input = X_test - np.expand_dims(means, 0)
# X_test_input /= np.expand_dims(stds, 0)
#
# predictions = clf.predict(X_test)
# print("F1 score:", f1_score(X_test, predictions, average='weighted'))

