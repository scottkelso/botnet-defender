from sklearn.utils import resample
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler, MaxAbsScaler
from scipy.sparse import hstack

import pandas as pd
import numpy as np


# TODO(jk): Stateful features

def encode_data(df):
    data = df.drop(columns=['category'])
    labels = df['category']

    print("Transforming categorical data to numeric...")
    # TODO(jk): Get OneHotEncoder working
    # https://stats.stackexchange.com/questions/267012/difference-between-preprocessing-train-and-test-set-before-and-after-splitting
    enc = OneHotEncoder(dtype=np.float64, sparse=True)
    data = enc.fit_transform(data, y=labels)

    # print("Normalizing data...")
    # scaler = StandardScaler(with_mean=False)
    # data = scaler.fit_transform(data, y=labels)

    print("Normalizing / Scaling data...")
    transformer = MaxAbsScaler().fit(data, y=labels)
    data = transformer.transform(data)
    return data, labels


def encode_unsupervised_data(data):
    print("Transforming categorical data to numeric...")
    enc = OneHotEncoder()
    data = enc.fit_transform(data)

    # TODO(jk): This needs to be the same instance as was used for training data
    print("Normalizing data...")
    scaler = StandardScaler(with_mean=False)
    # TODO(jk): Should be scaler.transform(data) -> we should have fit only once on training
    data = scaler.fit_transform(data)

    # print("Normalizing / Scaling data...")
    # transformer = MaxAbsScaler().fit(data)
    # data = transformer.transform(data)
    return data


def downsample(df, logging=False):
    if logging:
        print("Before resampling...")
        print(df.category.value_counts(), "\n")

    # # Separate majority and minority classes
    # df_majority = df[df.category == "Reconnaissance"]
    # df_minority = df[df.category == "Normal"]

    # Separate majority and minority classes
    df_reconnaissance = df[df.category == "Reconnaissance"]
    df_normal = df[df.category == "Normal"]
    minority_size = min(len(df_reconnaissance), len(df_normal))

    if len(df_reconnaissance) > len(df_normal):
        print("Downsampling Reconnaissance...")
        # Downsample majority class
        df_majority_downsampled = resample(df_reconnaissance,
                                           replace=False,  # sample without replacement
                                           n_samples=minority_size,  # to match minority class
                                           random_state=123)  # reproducible results

        # Combine minority class with downsampled majority class
        df_downsampled = pd.concat([df_majority_downsampled, df_normal])

    else:
        print("Downsampling Normal...")
        # Downsample majority class
        df_majority_downsampled = resample(df_normal,
                                           replace=False,  # sample without replacement
                                           n_samples=minority_size,  # to match minority class
                                           random_state=123)  # reproducible results

        # Combine minority class with downsampled majority class
        df_downsampled = pd.concat([df_majority_downsampled, df_reconnaissance])

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


# TODO(jk): Fix paths used here.
def load_test_data(path):
    print("Reading " + path + " as Test Traffic...")
    data = pd.read_csv('../../traffic/IoT/'+path, sep=';', dtype={'Sport': np.object, 'Dport': np.object})
    data = remove_bad_testing_data(data)
    return data


def load_test_data_full_path(path):
    print("Reading full path " + path + " as Test Traffic...")
    data = pd.read_csv("../"+path, sep=';', dtype={'Sport': np.object, 'Dport': np.object})
    data = remove_bad_testing_data(data)
    return data


def load_normal_data(path):
    data = load_test_data(path)
    data['category'] = "Normal"
    return data


def update_column_headers(data):
    data.columns = ['Flgs', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr',
       'Dport', 'TotPkts', 'TotBytes', 'State', 'SrcId', 'Dur',
       'Mean', 'StdDev', 'Sum', 'Min', 'Max', 'SrcPkts', 'DstPkts', 'SrcBytes',
       'DstBytes', 'Rate', 'SrcRate', 'DstRate', 'category']

    return data


def import_csvs():
    # TODO(jk): Convert into loop
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
    iot1 = load_normal_data('18-05-29.pcap.csv')
    print("Finished!\n")
    iot2 = load_normal_data('18-05-31.pcap.csv')
    print("Finished!\n")
    iot3 = load_normal_data('18-06-10.pcap.csv')
    print("Finished!\n")
    iot4 = load_normal_data('18-06-12.pcap.csv')
    print("Finished!\n")
    iot5 = load_normal_data('18-06-13.pcap.csv')
    print("Finished!\n")
    iot6 = load_normal_data('18-06-15.pcap.csv')
    print("Finished!\n")
    iot7 = load_normal_data('18-06-16.pcap.csv')
    print("Finished!\n")
    iot8 = load_normal_data('18-06-17.pcap.csv')
    print("Finished!\n")
    iot9 = load_normal_data('18-06-18.pcap.csv')
    print("Finished!\n")
    iot10 = load_normal_data('18-06-19.pcap.csv')
    print("Finished!\n")

    return pd.concat([os, ser, am, aur, sam, iot1, iot2, iot3, iot4, iot5, iot6, iot7, iot8, iot9, iot10], sort=True)


def get_data():
    data = import_csvs()
    data = downsample(data, logging=True)
    X, y = encode_data(data)
    return X, y


def preprocess_test_data(path):
    data = load_test_data_full_path(path)
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


def get_src_ip(file, flow):
    data = load_test_data(file)
    return data.SrcAddr[flow]
