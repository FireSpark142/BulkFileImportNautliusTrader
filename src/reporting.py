from random import random

import pandas as pd


def report(it):
    x = it.get_result().__dict__.get('stats_returns')
    y = it.get_result().__dict__.get('stats_pnls')
    df = pd.DataFrame(y).T.reset_index()
    df2 = df.drop(columns=['index'])
    df3 = df2.T

    df4 = pd.DataFrame(x, index=[0]).T
    df5 = pd.concat([df3, df4], axis=0).T
    df5.to_csv("../reports/" + str(random()), index=False)