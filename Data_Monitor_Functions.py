import os
import glob
import pandas as pd 
import numpy as np 
from os import listdir


#######  LOADING DCR & DCR_ITEM DATA ################################
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


########  GETTING DATA FROM MOVEIT ###################################
############ Bulk unzip files ##############
import zipfile
def unzipper(MoveItPath, DestinationPath):
	allFiles = glob.glob(os.path.join(MoveItPath, '*.zip'))
	os.makedirs(DestinationPath)
	for file_ in allFiles:
		zip_ref = zipfile.ZipFile(file_)
		zip_ref.extractall(DestinationPath)
		zip_ref.close()
	return("Unzipped!")


####### LOADING DATA FROM MOVEIT ####################################
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


########  DATA EXPORT ##################################################
# export a list of dataframes to multiple worksheets in one excel file
from pandas import ExcelWriter
def save_xls(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()


# For each field to be validated, if both 18-digit & 12-digit Id exist, keep the 18-digit one
def getRightId(x):
	if x['Id'].str.len().max() > x['Id'].str.len().min():
		x = x[x['Id'].str.len() == 18]
	return(x)













