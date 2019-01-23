from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from sklearn.utils import resample
from sklearn.preprocessing import OrdinalEncoder
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


# df['saddr'] = df['saddr'].apply(ip2int)
# df['daddr'] = df['daddr'].apply(ip2int)
# df['srcid'] = df['srcid'].apply(ip2int)


def load_os_csv():
    print("Reading OS_Scan CSV...")
    df = pd.read_csv('../data/OS_Scan.csv', sep=';')

    # Remove unneeded columns
    df = df.drop(
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

    # TODO(jk) Loop
    print("Dropping rows with wrong data...")
    # Drop all ipv6 and icmp packets
    df = df[~df.proto.str.contains("ipv6", na=False)]
    df = df[~df.proto.str.contains("icmp", na=False)]

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.sport = pd.to_numeric(df.sport.fillna(-1))
    df.dport = pd.to_numeric(df.dport.fillna(-1))

    # df = downsample(df)

    data = df.drop(columns=['category'])
    labels = df['category']

    # Numerate categorical data
    print("Transforming categorical data to numeric...")
    # TODO(jk): Refactor obj
    enc = OrdinalEncoder()
    data = enc.fit_transform(data, y=labels)

    print("Finished loading CSV.\n")

    return data, labels


def load_service_csv():
    print("Reading Service_Scan CSV...")
    df = pd.read_csv('../data/Service_Scan.csv', sep=';', dtype={'sport': np.object, 'dport': np.object})

    # Remove unneeded columns
    df = df.drop(
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

    # TODO(jk) Loop
    print("Dropping rows with wrong data...")
    # Drop all ipv6 and icmp packets
    df = df[~df.proto.str.contains("ipv6", na=False)]
    df = df[~df.proto.str.contains("icmp", na=False)]

    # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
    df = df[~df.sport.str.contains("xinetd", na=False)]

    # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
    df = df[~df.dport.str.contains("nut", na=False)]

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.sport = pd.to_numeric(df.sport.fillna(-1))
    df.dport = pd.to_numeric(df.dport.fillna(-1))

    # df = downsample(df)

    data = df.drop(columns=['category'])
    labels = df['category']

    # Numerate categorical data
    print("Transforming categorical data to numeric...")
    # TODO(jk): Refactor obj
    enc = OrdinalEncoder()
    data = enc.fit_transform(data, y=labels)

    print("Finished loading CSV.\n")

    return data, labels


def downsample(df):
    print("Before resampling...")
    print(df.category.value_counts(), "\n")

    # Separate majority and minority classes
    df_majority = df[df.category == "Reconnaissance"]
    df_minority = df[df.category == "Normal"]

    # Downsample majority class
    df_majority_downsampled = resample(df_majority,
                                       replace=False,  # sample without replacement
                                       n_samples=len(df_minority),  # to match minority class
                                       random_state=123)  # reproducible results

    # Combine minority class with downsampled majority class
    df_downsampled = pd.concat([df_majority_downsampled, df_minority])

    # Display new class counts
    print("After resampling...")
    print(df_downsampled.category.value_counts(), "\n")

    return df_downsampled


Xos, yos = load_os_csv()
Xser, yser = load_service_csv()

X = np.concatenate((Xos, Xser), axis=0)
y = np.concatenate((yos, yser), axis=0)

# Split the data into training, validation, and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("Training SVC Model...")
clf = svm.SVC(gamma='scale', probability=True, max_iter=1000)
clf.fit(X_train, y_train)

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
#
# dump(clf, 'filename.joblib')
