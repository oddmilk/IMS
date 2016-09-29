import os
import pandas as pd 
import numpy as np
import math
from pandas import ExcelWriter

# read in data
DF_ID = pd.read_excel('/Users/mengjichen/Desktop/TO_SPLIT.xlsx', "Sheet1")
# split data by number of rows: 1000 
groups = np.arange(math.ceil(len(DF_ID.index)/1000))
groups_list = []

for i in groups:
	temp = [groups[i]]*1000
	groups_list.append(temp) 

groups_list_flatten = [y for x in groups_list for y in x] 
groups_num_to_add = groups_list_flattned[0:len(DF_ID.index)]

# add group numbers to the data frame
DF = DF_ID
DF['groups'] = groups_num_to_add
DF['To_Split'] = DF['To_Split'] + ';'
DF_grouped = DF.groupby(DF.groups)

# split the data frame by group number:
writer = ExcelWriter('/Users/mengjichen/Desktop/iView_Process/Process.xlsx')
for (frameno, frame) in DF_grouped:
	frame.T.to_excel(writer, 'sheet%s' % frameno)

