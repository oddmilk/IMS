import os
import glob
import pandas as pd 
import numpy as np 
from os import listdir


# find current directory
cwd = os.getcwd()
wd = os.chdir('/Users/mengjichen/Desktop/Roche/201607')
listdir() # just to double check what's available in the cwd

# read multiple csv files and concatenate to one data frame
def readFile(path, pattern_, id_):
	allFiles = glob.glob(os.path.join(path, pattern_))
	frame = pd.DataFrame()
	list_ = []
	for file_ in allFiles:
		if os.stat(file_).st_size > 400:
			df = pd.read_csv(file_, index_col = None, sep = ";")
			list_.append(df)
			df['sourceFile'] = file_
			frame = pd.concat(list_)
			frame = frame.rename(columns = {id_: 'Id'})  
	return(frame)

SFDC_DCR = readFile('./SFDC_DCR', '*.CSV', '#Id')
SFDC_DCR_ITEM = readFile('./SFDC_ITEM', '*.CSV', '#Id')

OK_DCR = readFile('./OK_DCR', '*.CSV', '\ufeff"Id"')
OK_DCR_ITEM = readFile('./OK_ITEM', '*.CSV', '\ufeff"Id"')


# select columns in need
	# SFDC
SFDC_DCR_SUB = SFDC_DCR[['Id', 'Master_DCR_g__c', 'sourceFile', 'Type_g__c']]
SFDC_DCR_ITEM_SUB = SFDC_DCR_ITEM[['Id', 'Change_Request_ref_g__c', 'sourceFile', 
'Field_API_Name_g__c', 'Name', 
'Old_Field_Value_Text_g__c', 'Field_value_text_g__c']]

	# OK 
OK_DCR_SUB = OK_DCR[['Id', 'Master_DCR_g__c', 'sourceFile', 'Type_g__c', 'Remarks_g__c', 'Status_g__c']]
OK_DCR_ITEM_SUB = OK_DCR_ITEM[['Id', 'Change_Request_ref_g__c', 'sourceFile',
'Field_API_Name_g__c', 'Name', 
'Old_Field_Value_Text_g__c', 'Field_value_text_g__c']]


########  GETTING DATA FROM MOVEIT ###################################
############ Bulk unzip files ##############
import zipfile
allFiles = glob.glob(os.path.join('./moveit-export-2016-08-04/', '*.zip'))
for file_ in allFiles:
	zip_ref = zipfile.ZipFile(file_)
	zip_ref.extractall('./MOVEIT')
	zip_ref.close()

def readMoveIt(path, pattern_):
	allFiles = glob.glob(os.path.join(path, pattern_))
	frame = pd.DataFrame()
	list_ = []
	for file_ in allFiles:
		if os.stat(file_).st_size > 400:
			df = pd.read_table(file_, index_col = None, sep = "|")
			list_.append(df)
			df['sourceFile'] = file_
			frame = pd.concat(list_)
	return(frame)

MOVEIT = readMoveIt('./MOVEIT', '*.FLAT')

########## Subset data ##############
# Select columns of data 
DataIn = MOVEIT[['REQUEST_ID_CLIENT', 'REQUEST_DATE', 'REQUEST_COMMENT', 
'IND_FIRSTNAME', 'IND_LASTNAME', 'IND_GENDER_COD', 
'IND_CLASS_COD', 'ACT_ROLE_1',
'IND_ID_CEGEDIM', 'WKP_ID_CEGEDIM', 
'IND_SPECIALITY_1', 'IND_TITLE_COD', 'WKP_SPECIALITY_1', 
'WKP_PARENT_USUAL_NAME', 'sourceFile']]

DataIn["FULLNAME"] = DataIn["IND_LASTNAME"].map(str) + DataIn["IND_FIRSTNAME"].map(str)

# export a list of dataframes to multiple worksheets in one excel file
from pandas import ExcelWriter
def save_xls(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()

list_MV = [MOVEIT, DataIn]
list_SFDC = [SFDC_DCR, SFDC_DCR_ITEM, SFDC_DCR_SUB, SFDC_DCR_ITEM_SUB]
list_OK = [OK_DCR, OK_DCR_ITEM, OK_DCR_SUB, OK_DCR_ITEM_SUB]

save_xls(list_MV, './MOVEIT.xlsx')
save_xls(list_SFDC, './SFDC.xlsx')
save_xls(list_OK, './OK.xlsx')


############## DATA CHECK #################
# Total number of Master_DCR_g__c from SFDC
A = len(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master = pd.DataFrame(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master.columns = ['A_Master']

# Total number into MoveIt for OK to validate
B = len(DataIn.REQUEST_ID_CLIENT.unique())
B_Master = pd.DataFrame(MOVEIT.REQUEST_ID_CLIENT.unique())
B_Master.columns = ['B_Master']

# Date range of incoming client request 
R = [DataIn.REQUEST_DATE.min(), DataIn.REQUEST_DATE.max()]

# Number of DCR coming in after Jul.18

# CR approved automatically / out of scope by Conversion Tool (low priority)

# For CR that went into MOVEIT/OK for validation, subset SFDC ITEM data frame
SFDC_B = SFDC_DCR_ITEM[SFDC_DCR_ITEM.Change_Request_ref_g__c.isin(B_Master['B_Master'])]

# For the subset of master CR that went into OK for validation, subset rows by: Fields to validate & child ID
	# Field_API_Name_g__c
Fields_Cool = ['Administrative_Title_cn_g__pc', 
'Gender_g__pc', 
'LastName', 
'Professional_Type_g__pc', 
'Professional_Subtype_g__pc',
'Specialty_ref_g__c',
'Primary_Specialty_g__pc']

SFDC_B_In = SFDC_B[SFDC_B.Field_API_Name_g__c.isin(Fields_Cool)]

# Reshape MOVEIT data from wide to long
MoveIt_long = pd.melt(DataIn, 
	id_vars = ['REQUEST_ID_CLIENT'],
	value_vars = ['ACT_ROLE_1', # Administrative_Title_cn_g__pc
	'IND_GENDER_COD', # Gender_g__pc
	'FULLNAME', # LastName
	'IND_CLASS_COD', # Professional_Type_g__pc
	'IND_TITLE_COD', # Professional_Subtype_g__pc
	'WKP_ID_CEGEDIM', 
	'IND_SPECIALITY_1']) # Primary_Specialty_g__pc; Specialty_ref_g__c

list_SFDC_MoveIt = [SFDC_B_In, MoveIt_long]
save_xls(list_SFDC_MoveIt, "./SFDC_MOVEIT.xlsx")




# Remove unvalidated ID in each master DCR (ETL*)
	# filter DCRs by string length of Id
def getRightId(x):
	if x['Id'].str.len().max() > x['Id'].str.len().min():
		x = x[x['Id'].str.len() == 18]
	return(x)

SFDC_B_In_Final = SFDC_B_In.groupby('Change_Request_ref_g__c').apply(lambda x: getRightId(x)) # NOTE DCRs creating hospitals are not found here

list_DCR_INTO_OK = [SFDC_B_In, B_Master]
save_xls(list_DCR_INTO_OK, "./DCR_into_OK.xlsx")

# Summary stats
# Courtesy: Chris Albon
def get_stats(data):
	return {'min': group.min(),
	'max': group.max(),
	'count': group.count(),
	'mean': group.mean()}





























