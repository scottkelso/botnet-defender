from sklearn.utils import resample
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import pandas as pd
import numpy as np


# TODO(jk): Stateful features

def encode_data(df):
    data = df.drop(columns=['category'])
    labels = df['category']

    print("Transforming categorical data to numeric...")
    # TODO(jk): Get OneHotEncoder working
    enc = OneHotEncoder()
    data = enc.fit_transform(data, y=labels)

    # print("Normalizing data...")
    # scaler = StandardScaler()
    # data = scaler.fit_transform(data, y=labels)
    return data, labels


def encode_unsupervised_data(data):
    print("Transforming categorical data to numeric...")
    enc = OneHotEncoder()
    data = enc.fit_transform(data)

    print("Normalizing data...")
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return data


def downsample(df, logging=False):
    if logging:
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
    if logging:
        print("After resampling...")
        print(df_downsampled.category.value_counts(), "\n")

    return df_downsampled


def remove_bad_training_data(df):
    print("Dropping rows with wrong data...")
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
         'seq',
         'stime',
         'ltime'], axis=1
    )

    # Drop all man packets
    df = df[~df.proto.str.contains("man", na=False)]

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.sport = df.sport.fillna('-1')
    df.dport = df.dport.fillna('-1')
    df.dir = df.dir.fillna('-')

    return df


def remove_bad_testing_data(df):
    print("Dropping rows with wrong data...")
    # Remove unneeded columns
    df = df.drop(
        ['dCo',
         'sCo',
         'DstOui',
         'SrcOui',
         'DstMac',
         'SrcMac',
         'Seq',
         'StartTime',
         'LastTime'], axis=1
    )

    # Drop all man packets
    df = df[~df.Proto.str.contains("man", na=False)]

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.Sport = df.Sport.fillna('-1')
    df.Dport = df.Dport.fillna('-1')
    df.Dir = df.Dir.fillna('-')

    return df


def load_os_csv():
    print("Reading OS_Scan CSV...")
    data = pd.read_csv('../data/OS_Scan.csv', sep=';', dtype={'sport': np.object, 'dport': np.object})
    return remove_bad_training_data(data)


def load_service_csv():
    print("Reading Service_Scan CSV...")
    data = pd.read_csv('../data/Service_Scan.csv', sep=';', dtype={'sport': np.object, 'dport': np.object})
    return remove_bad_training_data(data)


def load_test_data(path):
    print("Reading " + path + " as Test Traffic...")
    data = pd.read_csv('../../traffic/IoT/'+path, sep=';', dtype={'Sport': np.object, 'Dport': np.object})
    data = remove_bad_testing_data(data)
    return data


def load_normal_data(path):
    data = load_test_data(path)
    # TODO(jk): Not adding column!
    data['category'] = "Normal"
    return data


def update_column_headers(data):
    data.columns = ['Flgs', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr',
       'Dport', 'TotPkts', 'TotBytes', 'State', 'SrcId', 'Dur',
       'Mean', 'StdDev', 'Sum', 'Min', 'Max', 'SrcPkts', 'DstPkts', 'SrcBytes',
       'DstBytes', 'Rate', 'SrcRate', 'DstRate', 'category']

    return data


def import_csvs():
    os = update_column_headers(load_os_csv())
    print("Finished!\n")
    ser = update_column_headers(load_service_csv())
    print("Finished!\n")
    am = load_normal_data('AmazonEcho.csv')
    print("Finished!\n")
    aur = load_normal_data('AuraSmartSleepSensor.csv')
    print("Finished!\n")
    sam = load_normal_data('SamsungGalaxyTab.csv')
    print("Finished!\n")

    return pd.concat([os, ser, am, aur, sam], sort=True)


def get_data():
    data = import_csvs()
    data = downsample(data, logging=False)
    X, y = encode_data(data)
    return X, y


def preprocess_test_data(path):
    data = load_test_data(path)
    if len(data) > 0:
        X = encode_unsupervised_data(data)
    else:
        X = None
    return X


def has_nan_values(data):
    for col in data.columns:
        print(col)
        if len(data[data[col].str.contains("nan", na=False)]) < 1:
            print("nan values")


# def drop_col_encode(df):
#     data = df.drop(columns=['category'])
#     labels = df['category']
#
#     for col in data.columns:
#
#         data = data.drop([col], axis=1)
#
#         try:
#
#             enc = OrdinalEncoder()
#             enc.fit_transform(data, y=labels)
#             print(col + " no error message!")
#         except:
#             print(col + " had an error message")

def check_types(data):
    for col in data.columns:
        print(data[col].apply(lambda x: type(x)).value_counts())
        print()
