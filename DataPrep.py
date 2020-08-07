import sys, os
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
            lines.append(obj)

    # serialize and deserialize??
    df = pd.DataFrame(lines)
    df = df.replace(r'^\s*$', 'NA', regex=True)

    return df

def data_prep(df):

    df.insert(6, 'overDraw', 0)
    df.insert(8, 'storeID', 'NA')
    df.insert(11, 'overSeas', 0)
    df.insert(18, 'addressChangeActivity', 0)
    df.insert(21, 'cvvMatch', 0)

    for i in range(0, len(df)):
        item = df.loc[i]

        merchantName = item['merchantName']
        merchantName = merchantName.split(' #')
        if len(merchantName) == 2:
            df.at[i, 'storeID'] = merchantName[1]
        df.at[i, 'merchantName'] = str(merchantName[0])

        availMoney = item['availableMoney']
        transAmt = item['transactionAmount']
        if availMoney - transAmt <= 0:
            df.at[i, 'overDraw'] = 1

        acqCountry = item['acqCountry']
        merchCountry = item['merchantCountryCode']
        if acqCountry != merchCountry:
            df.at[i, 'overSeas'] = 1

        dateOpen = item['accountOpenDate']
        dateAddrChange = item['dateOfLastAddressChange']
        if dateOpen != dateAddrChange:
            df.at[i, 'addressChangeActivity'] = 1

        cvvEntered = item['enteredCVV']
        cvvCard = item['cardCVV']
        if cvvEntered == cvvCard:
            df.at[i, 'cvvMatch'] = 1

    return df