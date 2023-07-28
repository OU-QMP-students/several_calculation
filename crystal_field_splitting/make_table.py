import re

import pandas as pd


def table(filepath: str) -> pd.DataFrame:
    row_data = pd.read_table(filepath, header=None)
    ind = row_data[0::2].reset_index(drop=True)
    data = row_data[1::2].reset_index(drop=True)

    ind = make_index(ind)
    data = make_data(data)

    datas = pd.concat([ind, data], axis=1)
    datas = datas.set_index("orbit bef")
    full_data = datas.sort_index()

    return full_data


def make_index(ind: pd.DataFrame.index) -> pd.DataFrame:
    # index
    patt = "[ -~].\([0-9]..\)[0-9][a-zA-Z].[0-9]"
    patt = re.compile(patt)
    for key, i in enumerate(ind.values):
        string = i[0]
        res = re.findall(patt, string)
        ind.loc[key, "orbit bef"] = res[0]
        ind.loc[key, "orbit aft"] = res[1]

    ind = ind.reset_index(drop=True)
    ind = ind.drop(columns=0)
    return ind


def make_data(data: pd.DataFrame):
    patt = "[0-9]+\.[0-9]+\ \+i.*"
    for key, i in enumerate(data.values):
        string = i[0]
        res = re.search(patt, string).group()
        res = res.replace(" +i*", "j")
        if "-" in res:
            val = eval(re.sub(" +", "", res))
        else:
            val = eval(re.sub(" +", "+", res))
        data.loc[key] = val
    data = data.reset_index(drop=True)

    return data
