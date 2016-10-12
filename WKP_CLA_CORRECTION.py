# data loading
import os
import pandas as pd 

dt = pd.read_table('/Users/mengjichen/Desktop/HCO_20161009.txt', usecols = [0, 5, 42, 66, 68])

# split data into HOSP and DEPT data
DEPT = dt[dt.WKP_STR_TYPE_COD.isin(['SER','SSE'])]
DEPT.columns = ['DEPT_ID_0', 'HOSP_ID', 'TYPE', 'DEPT_ID', 'DEPT_CLA']
DEPT2Merge = DEPT[['DEPT_ID', 'HOSP_ID', 'DEPT_CLA']]


HOSP = dt[dt.WKP_STR_TYPE_COD.isin(['GOR','ETA'])]
HOSP.columns = ['HOSP_ID_0', 'HOSP_ID_1', 'TYPE', 'HOSP_ID', 'HOSP_CLA']
HOSP2Merge = HOSP[['HOSP_ID_0', 'HOSP_CLA']]

test = pd.merge(DEPT2Merge, HOSP2Merge, left_on = 'HOSP_ID', right_on = 'HOSP_ID_0', how = 'left')

from pandas import ExcelWriter
writer = ExcelWriter('/Users/mengjichen/Desktop/output.xlsx')
test.to_excel(writer, 'Sheet1')
writer.save()
