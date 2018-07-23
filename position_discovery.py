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

from wordcloud import WordCloud
import jieba

mpl.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
mpl.rcParams['font.serif'] = ['SimHei', 'Arial']
mpl.rcParams['axes.unicode_minus'] = False
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

f, ax = plt.subplots(figsize = (12, 6))
ax = sns.barplot(x=bar_df["company_name"], y=bar_df["pos_id"], palette="rocket", ax=ax)
ax.set(xlabel='Company Name', ylabel='Position Count')
ax.set_xticklabels(ax.get_xticklabels(), rotation=85)
ax.tick_params(axis='x', width=30, labelsize=6)
plt.show()


ax = sns.distplot(df["salary_avg"], color="lightcoral")
ax.set(xlabel='Average Salary')
plt.show()

desc_str = ""
for row in df["pos_desc"]:
    desc_str += row

desc_str_utf8 = desc_str.encode("utf-8")
desc_jieba = jieba.cut(desc_str_utf8)
desc_split = " ".join(desc_jieba)
my_wordcloud = WordCloud().generate(desc_split)

font = r'C:\Windows\Fonts\simhei.ttf'
my_wordcloud = WordCloud(collocations=False, \
                         font_path=font, \
                         width=1400, height=1400, \
                         margin=2).generate(desc_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
