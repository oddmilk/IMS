'''
@Author: Oddmilk
@Date: Jan, 6, 2017
'''

# Import data 
import pandas as pd 
import numpy as np 
from pandas import ExcelWriter
import datetime

raw = pd.read_table('raw.txt', sep = ',', names = ['timestamp', 'source_id', 'question', 'text']) 

# Data extraction 
# time range: normal {Jul.15 - Aug.15}; peak {Aug.15 - Sep.15}
raw.timestamp = pd.to_datetime(raw.timestamp)
raw['year'] = raw.timestamp.dt.year
raw['month'] = raw.timestamp.dt.month
raw['day'] = raw.timestamp.dt.day

writer = pd.ExcelWriter('raw.xlsx')
raw.to_excel(writer, 'Sheet1')
writer.save()

raw_qq = pd.read_table('raw_qq.txt', names = ['text']).dropna()
raw_201608 = raw_qq[raw_qq.text.str.contains('2016-08')].reset_index()
raw_201608.columns = ['raw_index', 'non_text']
raw_201608_index = raw_201608.index
raw_201608_index_text = raw_201608_index + 1
raw_201608_text = raw_qq.iloc[raw_201608_index_text].reset_index()
# join index & text
raw_201608['text'] = raw_201608_text.text
# 2016-08-24
raw_0824 = raw_201608[raw_201608.non_text.str.contains("2016-08-24")].reset_index()
raw_0820 = raw_201608[raw_201608.non_text.str.contains("2016-08-20")].reset_index()


# for data in Aug basket, conduct NLP
import jieba
text_joined_0824 = ", ".join(raw_0824.text)
text_joined_0820 = ",".join(raw_0820.text)
seg_list_0824 = list(jieba.cut(text_joined_0824, cut_all = False))
seg_list_0820 = list(jieba.cut(text_joined_0820, cut_all = False))

from collections import Counter
top_0824 = Counter(seg_list_0824).most_common(500)
top_0820 = Counter(seg_list_0820).most_common(500)


# using list comprehension to find difference between the seg'ed lists for July and Aug
diff = [i for i in seg_list_0824 if not i in seg_list_0820]
comm = [i for i in seg_list_0824 if i in seg_list_0820]
diff_cnt = Counter(diff).most_common(500)
comm_cnt = Counter(comm).most_common(500)

