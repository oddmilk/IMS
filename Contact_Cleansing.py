# load data
import os
import glob
import pandas as pd 
import numpy as np 
from os import listdir
from pandas import ExcelWriter

Contact = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/Account_Contact_Location_201608.xls')
Target = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/目标医生_0818.xlsx')

# Data_Merged = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/Data_Merged.xlsx')

# inner join Target table and Contact table
Contact_for_cleansing = pd.merge(Target, Contact, left_on = 'SFDCID', right_on = 'Contact ID', how = 'left')

from pandas import ExcelWriter
writer = ExcelWriter('/Users/mengjichen/Desktop/ID_mapping/Contact/Contact_Pool_Roche.xlsx')
Contact_for_cleansing.to_excel(writer, 'Sheet1')

Contact_OK_ID = Contact['OneKey Individual ID'].unique()

#########################################################
Roche_Contact = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/Contact_Pool_Roche.xlsx')

# Bulk import OK contact 
def readExcelFile(path, pattern_):
	allFiles = glob.glob(os.path.join(path, pattern_))
	frame = pd.DataFrame()
	list_ = []
	for file_ in allFiles:
		if os.stat(file_).st_size > 400:
			df = pd.read_excel(file_)
			list_.append(df)
			frame = pd.concat(list_)
	return(frame)

OK_path = '/Users/mengjichen/Desktop/ID_mapping/Contact/OK_Contact/'
OK_pattern_ = '*.xls'
OK_Contact = readExcelFile(OK_path, OK_pattern_)

# Number of records comparison: Roche vs. Onekey
len(Roche_Contact['OneKey Individual ID'].unique())
len(Roche_Contact['医生: OneKey Workplace/Individual ID'].unique())
len(OK_Contact.index)

# Data fields subsetting
Roche = Roche_Contact[['SFDCID', 'CONTACTNAME', 'OneKey Individual ID', '医生: 主修专业', '医生: 性别', '客户名', '科室/部门', '职位', '医生: 专业类型', '医生: 学术职称']]
Roche.columns = ['SFDCID', 'NAME', 'OK_ID', 'ROCHE_SP', 'GEN', 'HOSPITAL', 'DEPT', 'ROLE', 'PROF_TYPE', 'PROF_TITLE']

OK_Contact['OK_NAME'] = OK_Contact.Ind_Lastname + OK_Contact.Ind_Firstname
OK_Contact.columns = ['HOSPITAL_OK_ID', 'HOSPITAL_OK', 'DEPT_OK', 'AFF_POS', 'AFF_OK_ID', 'OK_ID', 'F_NAME', 'L_NAME', 'GEN_OK', 'PROF_TYPE_OK', 'PROF_TITLE_OK', 'SP_COD_OK', 'SP_OK', 'NAME_OK']

# Data merging by OK_ID
Data_Merged = pd.merge(Roche, OK_Contact, on = 'OK_ID', how = 'outer')

# Data field comparison
Data_Merged['HOSPITAL_COMP'] = np.where(Data_Merged.HOSPITAL_OK == Data_Merged.HOSPITAL, "Y", "N")
Data_Merged['NAME_COMP'] = np.where(Data_Merged.NAME_OK == Data_Merged.NAME, "Y", "N")
Data_Merged['GEN_COMP'] = np.where(Data_Merged.GEN_OK == Data_Merged.GEN, "Y", "N")
Data_Merged['PROF_TYPE_COMP'] = np.where(Data_Merged.PROF_TYPE_OK == Data_Merged.PROF_TYPE, "Y", "N")

# Filter out data that have no OK ID
Merged_Sub = Data_Merged[~Data_Merged["OK_ID"].str.contains("-", na = False)] # returning rows with valid Onekey ID only
Merged_Sub_2 = Merged_Sub[~Merged_Sub.OK_ID.isnull()]

DEPT_MAP = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/Client_DEPT_SP_Mapping_201607.xlsx')
DEPT_MAP.columns = ['Client_DEPT_ID', 'DEPT', 'SP', 'SP_CODE']
Merged_Sub_3 = Merged_Sub_2[Merged_Sub_2.DEPT.isin(DEPT_MAP.DEPT)]

# Hospital Check

# Name Check (Chinese Character to Pinyin converter)

# Data subsetting



Batch_1 = Merged_Sub_2[Merged_Sub_2.HOSPITAL_COMP.str.contains("N") | Merged_Sub_2.NAME_COMP.str.contains("N")]

writer = ExcelWriter('/Users/mengjichen/Desktop/ID_mapping/Contact/Data_Merged.xlsx')
Data_Merged.to_excel(writer, 'Sheet1')
Batch_1.to_excel(writer, 'Sheet2')
writer.save()




