import os
from os import path
import requests, zipfile, io
import json
import pandas as pd
import numpy as np

def get_data(url):

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

    file_name = z.namelist()[0]
    base = path.splitext(file_name)[0]
    os.rename(file_name, base + ".json")

    new_file_name = base + ".json"

    return new_file_name

def get_databuffer(fname):

    lines = []

    with open(fname, "r") as fp:
        for line in fp:
            obj = json.loads(line)
            # load(s) -> serialize
            # dump(s) -> deserialize
            lines.append(obj)

    df = pd.DataFrame(lines)
    df = df.replace(r'^\s*$', 'NA', regex=True)

    return df

def data_prep(df):

    new_features = []

    new_features.append('overDraw')
    df.insert(6, 'overDraw', 0)
    df['overDraw'] = np.where(df['availableMoney'] - df['transactionAmount'] <= 0, 1, df['overDraw'])

    new_features.append('storeID')
    df.insert(8, 'storeID', 'NA')
    for i in range(0, len(df)):
        item = df.loc[i]
        merchantName = item['merchantName']
        merchantName = merchantName.split(' #')
        if len(merchantName) == 2:
            df.at[i, 'storeID'] = merchantName[1]
        df.at[i, 'merchantName'] = str(merchantName[0])

    new_features.append('overSeas')
    df.insert(11, 'overSeas', 0)
    df['overSeas'] = np.where(df['acqCountry'] != df['merchantCountryCode'], 1, df['overSeas'])

    new_features.append('addressChangeActivity')
    df.insert(18, 'addressChangeActivity', 0)
    df['addressChangeActivity'] = np.where(df['dateOfLastAddressChange'] != df['accountOpenDate'], 1, df['addressChangeActivity'])

    new_features.append('cvvMatch')
    df.insert(21, 'cvvMatch', 0)
    df['cvvMatch'] = np.where(df['cardCVV'] == df['enteredCVV'], 1, df['cvvMatch'])

    df['cardPresent'] = df['cardPresent'].astype(int)
    df['expirationDateKeyInMatch'] = df['expirationDateKeyInMatch'].astype(int)
    df['isFraud'] = df['isFraud'].astype(int)

    print(new_features)
    return df

def add_dummies(df, cat_vars):

    columns = df.columns.values
    # cat_vars = everything not excluded
    for var in cat_vars:
        # print(var)
        cat_list = 'var'+'_'+var
        cat_list = pd.get_dummies(df[var], prefix=var)
        # print(cat_list)
        # print('-----')
        df = df.join(cat_list)

    data_vars = df.columns.values.tolist()
    to_keep = [i for i in data_vars if i not in cat_vars]
    dummies = [i for i in data_vars if i not in columns]
    df_final = df[to_keep]

    return df_final, dummies
