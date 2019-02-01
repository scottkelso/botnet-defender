from sklearn.utils import resample
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

import pandas as pd
import numpy as np


def load_os_csv():
    print("Reading OS_Scan CSV...")
    data = pd.read_csv('../data/OS_Scan.csv', sep=';')
    return remove_bad_data(data)


def load_service_csv():
    print("Reading Service_Scan CSV...")
    data = pd.read_csv('../data/Service_Scan.csv', sep=';', dtype={'sport': np.object, 'dport': np.object})
    return remove_bad_data(data)


def load_test_data(path):
    print("Reading " + path + " as Test Traffic...")
    data = pd.read_csv('../../traffic/IoT/'+path, sep=';', dtype={'Sport': np.object, 'Dport': np.object})
    data = remove_bad_data_normal(data)
    return data


def load_normal_data(path):
    data = load_test_data(path)
    data.category = "Normal"
    return data


def remove_bad_data(df):
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
         'seq'], axis=1
    )

    # Drop all ipv6 and icmp packets
    df = df[~df.proto.str.contains("ipv6", na=False)]
    df = df[~df.proto.str.contains("icmp", na=False)]

    # https://en.wikipedia.org/wiki/Xinetd
    df = df[~df.sport.str.contains("xinetd", na=False)]

    # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
    df = df[~df.dport.str.contains("nut", na=False)]

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.sport = pd.to_numeric(df.sport.fillna(-1))
    df.dport = pd.to_numeric(df.dport.fillna(-1))

    return df


# TODO(jk): Better naming
def remove_bad_data_normal(df):
    print("Dropping rows with wrong data...")
    # Remove unneeded columns
    df = df.drop(
        ['dCo',
         'sCo',
         'DstOui',
         'SrcOui',
         'DstMac',
         'SrcMac',
         'Seq'], axis=1
    )

    # Drop all ipv6, icmp & llc packets
    df = df[~df.Proto.str.contains("ipv6", na=False)]
    df = df[~df.Proto.str.contains("icmp", na=False)]
    df = df[~df.Proto.str.contains("llc", na=False)]
    df = df[~df.Proto.str.contains("man", na=False)]

    # TODO(jk): Make ports null or negative number represented instead of dropping record

    # https://en.wikipedia.org/wiki/Xinetd
    df = df[~df.Sport.str.contains("xinetd", na=False)]

    # https://networkupstools.org/docs/user-manual.chunked/ar01s09.html
    df = df[~df.Dport.str.contains("nut", na=False)]

    df = df[~df.Sport.str.contains("domain", na=False)]
    df = df[~df.Dport.str.contains("domain", na=False)]

    df = df[~df.Sport.str.contains("bootpc", na=False)]
    df = df[~df.Dport.str.contains("bootps", na=False)]
    df = df[~df.Sport.str.contains("bootps", na=False)]
    df = df[~df.Dport.str.contains("bootpc", na=False)]

    df = df[~df.Dport.str.contains("http", na=False)]
    df = df[~df.Dport.str.contains("ntp", na=False)]
    df = df[~df.Dport.str.contains("xmpp-client", na=False)]
    df = df[~df.Dport.str.contains("mdns", na=False)]
    df = df[~df.Dport.str.contains("imaps", na=False)]

    # Amazon Echo
    # Dport - domain, http, https, bootps, ntp
    # Sport - domain, bootpc

    # Aura Smart Sleep ensor
    # Dport - xmpp-client, mdns

    # Reset indexes that now have missing values
    df = df.reset_index(drop=True)

    # Convert NA values to port -1
    df.Sport = pd.to_numeric(df.Sport.fillna(-1))
    df.Dport = pd.to_numeric(df.Dport.fillna(-1))

    return df


def encode_data(df):
    data = df.drop(columns=['category'])
    labels = df['category']

    print("Transforming categorical data to numeric...")
    enc = OrdinalEncoder()
    data = enc.fit_transform(data, y=labels)

    print("Normalizing data...")
    scaler = StandardScaler()
    data = scaler.fit_transform(data, y=labels)
    return data, labels


def encode_unsupervised_data(data):
    print("Transforming categorical data to numeric...")
    enc = OrdinalEncoder()
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


def get_data():
    data = import_csvs()
    data = downsample(data, logging=True)
    X, y = encode_data(data)

    return X, y


def update_column_headers(data):
    data.columns = ['StartTime', 'Flgs', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr',
       'Dport', 'TotPkts', 'TotBytes', 'State', 'SrcId', 'LastTime', 'Dur',
       'Mean', 'StdDev', 'Sum', 'Min', 'Max', 'SrcPkts', 'DstPkts', 'SrcBytes',
       'DstBytes', 'Rate', 'SrcRate', 'DstRate', 'category']

    return data


def import_csvs():
    # TODO(jk): Return array of data
    os = update_column_headers(load_os_csv())
    ser = update_column_headers(load_service_csv())
    am = load_normal_data('AmazonEcho.csv')
    aur = load_normal_data('AuraSmartSleepSensor.csv')
    sam = load_normal_data('SamsungGalaxyTab.csv')

    return pd.concat([os, ser, am, aur, sam], sort=True)


def preprocess_test_data(path):
    data = load_test_data(path)
    # TODO(jk): Stateful features
    if len(data) > 0:
        X = encode_unsupervised_data(data)
    else:
        X = None
    return X


# os.shape
# (360348, 27)

# am.shape
# (8953, 26)

# os.columns
# Index(['stime', 'flgs', 'proto', 'saddr', 'sport', 'dir', 'daddr', 'dport',
#        'pkts', 'bytes', 'state', 'srcid', 'ltime', 'dur', 'mean', 'stddev',
#        'sum', 'min', 'max', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate',
#        'srate', 'drate', 'category'],
#       dtype='object')

# am.columns
# Index(['StartTime', 'Flgs', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr',
#        'Dport', 'TotPkts', 'TotBytes', 'State', 'SrcId', 'LastTime', 'Dur',
#        'Mean', 'StdDev', 'Sum', 'Min', 'Max', 'SrcPkts', 'DstPkts', 'SrcBytes',
#        'DstBytes', 'Rate', 'SrcRate', 'DstRate'],
#       dtype='object')
