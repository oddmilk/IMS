'''

GSK follow up
@Author: Oddmilk
Date: Jan 10, 2017

'''

# load data (csv format as provided) into a list of data frames
import pandas as pd 
import numpy as np 
import os
import re
import sys
from pandas import ExcelWriters

path = os.getcwd()
files = os.listdir(path)
files_csv = [f for f in files if f[-3:] == 'csv']

raw_list = []

for f in files_csv:
    data = pd.read_csv(f, sep = ",")
    raw_list.append(data)

for i in range(len(raw_list)):
    writer = pd.ExcelWriter(os.path.join(str(i) + '.xlsx'))
    raw_list[i].to_excel(writer, 'Sheet1')
    writer.save()

# Data subsetting
email_detail = raw_list[0] # PK: EMAIL_ID
email_brief = raw_list[1]

email_detail_sa = email_detail[email_detail.PROD_NAME == "Seretide Asthma"]
email_detail_sa_valid = email_detail_sa[email_detail_sa['Call_ID'].notnull()]

# import user_doctor_id, active_users
# Join user_doctor_id and active_users

def dummyCreate(x):
	if pd.notnull(x):
		return 1
	else: 
		return 0

user_doctor_id = pd.read_excel("user_doctor_id.xlsx")
active_users = pd.read_excel("activeuser.xls")

portal_active_dcr = pd.merge(user_doctor_id, active_users, how = 'left')
portal_active_dcr['is_active'] = portal_active_dcr.Active_Date.apply(lambda x: dummyCreate(x))

# Join portal_active_dcr with email_detail_sa
portal_active_only = portal_active_dcr[portal_active_dcr.is_active == 1][['User_ID','Doctor_ID']].drop_duplicates()
email_detail_sa_active = pd.merge(email_detail_sa_valid, portal_active_only, how = 'left', left_on = 'DOCTOR_ID', right_on = 'Doctor_ID')
email_detail_sa_active['is_active'] = email_detail_sa_active.Doctor_ID.apply(lambda x: dummyCreate(x))

# create a categorical variable on email delivery & open
	# 1: mail delivered & opened
	# 2: mail delivered but not opened
	# 0: delivery failure
email_detail_sa_active['mail_delivery_open'] = np.where(((email_detail_sa_active.IS_Delivery == 1) & (email_detail_sa_active.MAIL_IS_OPEN == 1)), 1,
	np.where(((email_detail_sa_active.IS_Delivery == 1) & (email_detail_sa_active.MAIL_IS_OPEN == 0)),2,0))


# join email detail table with email brief
email_sa_active = email_detail_sa_active.merge(email_brief[['EMAIL_ID','DOCU_ID','DOCU_IS_OPEN']], on = 'EMAIL_ID', how = 'inner')

email_sa_active['step_three'] = np.where((email_sa_active['mail_delivery_open'] == 1) & (email_sa_active['DOCU_IS_OPEN'] == 1), 1, 0)

# get a subset of columns
reg_data = email_sa_active[['EMAIL_ID', 'DOCTOR_ID', 'DOCTOR_NATIONAL_SEGMENT', 'is_active', 'mail_delivery_open', 'DOCU_ID', 'step_three']].drop_duplicates()



# Group data by doctor (one doctor can receive multiple emails)
reg_data_grp = reg_data.groupby('DOCTOR_ID')
# for each unique doctor, count emails received
t_0 = reg_data_grp['EMAIL_ID'].apply(lambda x: len(x.unique()))
dcr_email = pd.DataFrame(t_0).reset_index()
dcr_email.columns = ['DOCTOR_ID', 'email_received']

# for each unique doctor (regardless of his/her activity on portal), count the number of unique documents opened
t_1 = reg_data_grp['DOCU_ID'].apply(lambda x: len(x))
dcr_doc = pd.DataFrame(t_1).reset_index()
dcr_doc.columns = ['DOCTOR_ID', 'doc_received']

t_2 = reg_data_grp['DOCU_ID'].apply(lambda x: len(x.unique()))
dcr_doc_unique = pd.DataFrame(t_2).reset_index()
dcr_doc_unique.columns = ['DOCTOR_ID', 'unique_doc_received']

# for each unique doctor, count email attachments they've opened
doc_open = pd.crosstab(reg_data['DOCTOR_ID'], reg_data['step_three'])
doc_open.columns = ['unopen', 'open']
doc_open = doc_open.reset_index()

# merge multiple data frames (to be func'ed)
dcr = dcr_email.merge(dcr_doc, how = 'inner')
dcr = dcr.merge(dcr_doc_unique, how = 'inner')
dcr = dcr.merge(doc_open, how = 'inner')

# merge data
dcr_active = reg_data[['DOCTOR_ID', 'is_active', 'DOCTOR_NATIONAL_SEGMENT']].drop_duplicates('DOCTOR_ID')
reg_data_final = dcr.merge(dcr_active, how = 'inner')
reg_data_final['doc_open_rate'] = reg_data_final['open']/reg_data_final['doc_received']

writer = pd.ExcelWriter('/Users/mengjichen/Desktop/Advanced_Analytics/MCM/data_tables/Output/reg_data_final.xlsx')
reg_data_final.to_excel(writer, 'sheet1')
writer.save()


# Explorative data analysis
import matplotlib.pyplot as plt
import seaborn as sns

reg_data_final.DOCTOR_NATIONAL_SEGMENT = pd.Series(reg_data_final.DOCTOR_NATIONAL_SEGMENT, dtype = "category")
reg_data_final.DOCTOR_NATIONAL_SEGMENT = reg_data_final.DOCTOR_NATIONAL_SEGMENT.cat.reorder_categories(['A','B','C','D','N','KDM'], ordered = True)

# put multiple distribution on the same plot
f0 = plt.hist(reg_data_final.is_active)
plt.savefig('mail_portal_activity.pdf')
plt.clf()

f1 = sns.barplot(x = "is_active", y = "doc_open_rate", hue = "DOCTOR_NATIONAL_SEGMENT", data = reg_data_final,
	palette = {"A":"#f2f9bc", "B":"#bbe4b5", "C":"#57bec0", "D":"#1d8cbe", "KDM":"#2166ab", "N":"#1c2d83"})
plt.savefig(('open_rate_against_dcr_segment.pdf'))
plt.clf()


# logistic regression model fitting
import statsmodels.api as sm

# create dummy variables for the categorical variable (DOCTOR_NATIONAL_SEGMENT) for the ease of result interpretation
dummy_segments = pd.get_dummies(reg_data_final['DOCTOR_NATIONAL_SEGMENT'], prefix = 'segment')
cols_to_keep = ['is_active', 'unique_doc_received', 'doc_open_rate']
data = reg_data_final[cols_to_keep].join(dummy_segments.ix[:, 'segment_B':])

# manually add the intercept
data['intercept'] = 1.0 

train_cols = data.columns[1:]
logit = sm.Logit(data['is_active'], data[train_cols])
result = logit.fit()
print(result.summary())


from statsmodels.graphics.mosaicplot import mosaic
from matplotlib import pylab





# logistic regression
import statsmodels.api as sm
import pylab as pl






