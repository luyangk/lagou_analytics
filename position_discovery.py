# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 07:54:29 2018

@author: A7XFAZZ
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
mpl.rcParams['font.serif'] = ['SimHei', 'Arial']
sns.set_style("whitegrid",{"font.sans-serif":['simhei', 'Arial']})

pd.set_option('display.float_format', lambda x: '%.2f' % x)

df = pd.read_csv(
        "C:/Users/a7xfazz/Documents/Github/lagou_analytics/lagou/pos_output.csv",
        encoding="gb2312")

df["salary_min"] = df["salary"].apply(lambda x: int(x.split('-')[0].replace('k','')))
df["salary_max"] = df["salary"].apply(lambda x: int(x.split('-')[1].replace('k','')))
df["salary_avg"] = (df["salary_min"] + df["salary_max"])/2



bar_df = df.groupby(by="company_name", as_index=False).agg({"pos_id":"count"}).sort_values( \
                   by=["pos_id"], ascending=False)

f, ax1 = plt.subplots(1, 1, figsize=(9,7), sharex=True)
sns.barplot(x=bar_df["company_name"], y=bar_df["pos_id"], palette="rocket", ax=ax1)
