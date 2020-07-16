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

    new_file_name = base+".json"

    return new_file_name

def get_databuffer(fname):
    lines = []
    with open(fname, "r") as fp:
        for line in fp:
            obj = json.loads(line)
            lines.append(obj)

    data = pd.DataFrame(lines)

    data = data.replace(r'^\s*$', np.nan, regex=True)
    print(data.loc[1])