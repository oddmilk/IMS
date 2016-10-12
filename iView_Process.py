import os
import pandas as pd 
import numpy as np
import math
from pandas import ExcelWriter
import csv

# read in data
DF_ID = pd.read_excel('/Users/mengjichen/Desktop/20161012_SHP.xlsx', "Sheet1")
# split data by number of rows: 1000 
groups = np.arange(math.ceil(len(DF_ID.index)/1000))
groups_list = []

for i in groups:
	temp = [groups[i]]*1000
	groups_list.append(temp) 

groups_list_flatten = [y for x in groups_list for y in x] 
groups_num_to_add = groups_list_flatten[0:len(DF_ID.index)]

# add group numbers to the data frame
DF = DF_ID
DF['groups'] = groups_num_to_add
DF['To_Split'] = DF['To_Split'] + ';'
DF_grouped = DF.groupby(DF.groups)

# split the data frame by group number:
writer = ExcelWriter('/Users/mengjichen/Desktop/iView_Process/20161012_SHP_Flattened.xlsx')
for (frameno, frame) in DF_grouped:
	x = frame.To_Split.str.cat()
	y = pd.Series([x])
	z = pd.DataFrame([y])
	z.to_excel(writer, 'sheet%s' % frameno)
	
writer.save()

