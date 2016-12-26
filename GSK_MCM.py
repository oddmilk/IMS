'''
Analysis for GSK China marketing 
================================================================================

Project time: Oct - Nov. 2016
@Author: oddmilk

'''

################################################################################

# Load data
import os.path
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from datetime import datetime, date, time
from operator import methodcaller

# Data on iDA
WORKCALL = pd.read_excel(os.path.join(Root_Dir, In, 'iDA/workcall.xlsx'))
WORKFEEDBACK = pd.read_excel(os.path.join(Root_Dir, In, 'iDA/WORKFEEDBACK.xlsx'))
MATERIAL = pd.read_excel(os.path.join(Root_Dir, In, 'iDA/material.xlsx'))
REGION = pd.read_excel(os.path.join(Root_Dir, In, 'iDA/region.xlsx'))
iDA_DCR_ID = pd.read_excel(os.path.join(Root_Dir, In, 'iDA/iDA_DCR_ID.xlsx'))

# Data on Portal
EDM_Click = pd.read_table(os.path.join(Root_Dir, In, 'Portal/EDM_Click.txt')) # EDM_ID, CampaignID, Email
MRM_User = pd.read_excel(os.path.join(Root_Dir, In, 'Portal/User_Doctor.xlsx')) # PK: User_ID
MRM_Content = pd.read_excel(os.path.join(Root_Dir, In, 'Portal/MRM_Content.xls')) # PK: Content_ID
MRM_PageView = pd.read_excel(os.path.join(Root_Dir, In, 'Portal/MRM_Page_View.xls')) # PK: Page_View_ID
Portal_DCR_ID = pd.read_excel(os.path.join(Root_Dir, In, 'Portal/Portal_DCR_ID.xlsx')) 

ACTIVE_DCR_PORTAL = pd.read_excel(os.path.join(Root_Dir, In, 'Portal/activeuser.xls'))
ACTIVE_DCR_PORTAL_UNIQUE = ACTIVE_DCR_PORTAL.User_ID.unique()


# Doctors on both iDA and Portal
iDA_DCR_ID.columns = ['Doctor_ID']
iDA_DCR_ID.Doctor_ID = iDA_DCR_ID.Doctor_ID.astype(str)
iDA_Portal_DCR_ID = iDA_DCR_ID.merge(Portal_DCR_ID, on = 'Doctor_ID', how = 'inner')

# Doctors on both channels with a visit ID
DCR_Portal_User = MRM_PageView.groupby('User_ID') # Unique users on portal (each user can have multiple visits)
Portal_Visits = DCR_Portal_User['Visit_ID'].apply(lambda x: len(x.unique())) # Unique visits for each user ID
Portal_Visits = pd.DataFrame(Portal_Visits)
Portal_Visits.reset_index(inplace = True)

Portal_PV = DCR_Portal_User['Page_View_ID'].apply(lambda x: len(x.unique()))
Portal_PV = pd.DataFrame(Portal_PV)
Portal_PV.reset_index(inplace = True)

Portal_User_Perf = Portal_Visits.merge(Portal_PV, on = 'User_ID', how = 'inner')
Portal_User_Perf.columns = ['User_ID', 'Visit_Count', 'PageView_Count']

DCR_iDA_Portal_User = iDA_Portal_DCR_ID.merge(Portal_User_Perf, on = 'User_ID', how = 'inner')
DCR_iDA_Portal_User['PV_Visit_Ratio'] = DCR_iDA_Portal_User.PageView_Count/DCR_iDA_Portal_User.Visit_Count

Email_1 = DCR_iDA_Portal_User.Email.unique()
Email_2 = EDM_Click.Email.unique()
DCR_iDA_Portal_EDM_Click = set(Email_1).intersection(Email_2) # Active portal users who have clicked an EDM

DCR_iDA_Portal_User['EDM_Clicked'] = np.where(DCR_iDA_Portal_User.Email.isin(DCR_iDA_Portal_EDM_Click), 1, 0) # Whether one has EDM click

# Join Portal profile with iDA profile
DCR_iDA_Perf = Doctor_Table[['DOCTOR_ID','DOCTOR_NATIONAL_SEGMENT','Int_Segment','DEPARTMENT','REGION','CALL_COUNT','KM_COUNT','AVG_CALL_DURATION','AVG_PG_DURATION']]
DCR_iDA_Perf.DOCTOR_ID = DCR_iDA_Perf.DOCTOR_ID.astype(str)
DCR_iDA_Portal_Perf = DCR_iDA_Portal_User.merge(DCR_iDA_Perf, left_on = 'Doctor_ID', right_on = 'DOCTOR_ID', how = 'inner')

writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'doctor_profile.xlsx'))
DCR_iDA_Portal_Perf.to_excel(writer, 'Sheet1')
writer.save()


# Portal visit table #
doctor_scope = DCR_iDA_Portal_User.User_ID.unique()
visit_scope = MRM_PageView[MRM_PageView.User_ID.isin(doctor_scope.User_ID)]
visit = visit_scope.groupby('Visit_ID')['Page_View_ID'].apply(lambda x: len(x.unique())) # Unique PV in a visit
visit = pd.DataFrame(visit)
visit.reset_index(inplace = True)
visit.columns = ['Visit_ID', 'PV_Count']
visit_timestamp = visit_scope[['Visit_ID', 'DateTime']].drop_duplicates()
visit_timestamp = visit_timestamp.groupby('Visit_ID').first()
visit_timestamp['visit_ymd'] = visit_timestamp.DateTime.apply(lambda x: str(x)[0:8])
visit_timestamp['visit_hr'] = visit_timestamp.DateTime.apply(lambda x: str(x)[-2:])
visit_timestamp.reset_index(inplace = True)
visit_table = visit_timestamp.merge(visit, on = 'Visit_ID')

portal_visit = visit_table.merge(Visit_User, on = 'Visit_ID', how = 'left')
portal_visit = portal_visit.merge(doctor_profile[['User_ID','Int_Segment','REGION']], 
	on = 'User_ID', how = 'left')

####################################################################################################
# Simple plotting #
import matplotlib.pyplot as plt
import seaborn as sns

# Doctor data against portal perf
p1 = sns.stripplot(x = "PV_Visit_Ratio", y = "REGION", data = doctor_profile, jitter = 0.05, linewidth = 1)
p2 = sns.stripplot(x = "PV_Visit_Ratio", y = "REGION", hue = "KM_COUNT", data = doctor_profile, 
	jitter = True, linewidth = 1, palette = "Set2", split = True)
p3 = sns.factorplot(x = "REGION", y = "PV_Visit_Ratio", hue = "KM_COUNT", kind = "bar", ci = None, data = doctor_profile)

# Visit hour against page count
p4 = sns.factorplot(x = "visit_hr", y = "PV_Count", ci = None, data = portal_visit)
p5 = sns.factorplot(x = "visit_hr", y = "PV_Count", hue = "Int_Segment", ci = None, data = portal_visit, size = 4, legend = False)
plt.legend(loc = 'upper left')
plt.xlabel('visit hour')
plt.ylabel('PageViews')
plt.title('PageView/Time by Doctor National Segment')

p5 = sns.factorplot(x = "visit_hr", y = "PV_Count", hue = "REGION", ci = None, data = portal_visit, size = 4, legend = False)
plt.legend(loc = 'upper left')
plt.xlabel('visit hour')
plt.ylabel('PageViews')
plt.title('PageView/Time by REGION')

# Portal-only physicians #
	# region against types of campaign #
	# raw data: content
test = pd.crosstab(content.region, [content.campaign_type, content.department])
test = test.reset_index()

test = content.groupby(['region', 'campaign_type', 'grade']).apply(lambda x: len(x))
test = pd.DataFrame(test)
test.reset_index(inplace = True)
test.columns = ['region','campaign_type','grade','unique_PV']

g = sns.factorplot(x = "region", y = "unique_PV", hue = "dept", col = "campaign_type",
	data = test, capsize = .2, palette = "YlGnBu_d", size = 6, aspect = .75)
g.despine(left = True)

# setting the positions and width for the bars
pos = list(range(len(test['3rd party literature'])))
width = 0.25

# plotting the bars
fig, ax = plt.subplots(figsize = (20, 10))

# Creating a bar with 3rd party literature data in position pos,
plt.bar(pos,
	test['3rd party literature'],
	width,
	alpha = 0.5,
	color = '#EE3224',
	label = test['region'][0])

plt.bar([p + width for p in pos],
	test['academic frontier'],
	width,
	alpha = 0.5,
	color = '#F78F1E',
	label = test['region'][1])

plt.bar([p + width*2 for p in pos],
	test['g-brand'],
	width,
	alpha = 0.5,
	color = '#FFC222',
	label = test['region'][2])

plt.bar([p, width*3 for p in pos],
	test['g-lecture'],
	width,
	alpha = 0.5,
	color = '#008080',
	label = test['region'][3])


plt.bar([p, width*4 for p in pos],
	test['g-link'],
	width,
	alpha = 0.5,
	color = '#003366',
	label = test['region'][4])

plt.bar([p, width*5 for p in pos],
	test['g-seminar'],
	width,
	alpha = 0.5,
	color = '#468499',
	label = test['region'][5])

plt.bar([p, width*6 for p in pos],
	test['g-video'],
	width,
	alpha = 0.5,
	color = '#ff6666',
	label = test['region'][6])

plt.bar([p, width*7 for p in pos],
	test['g-webinar'],
	width,
	alpha = 0.5,
	color = '#ccff00',
	label = test['region'][7])

plt.bar([p, width*8 for p in pos],
	test['ime'],
	width,
	alpha = 0.5,
	color = '#ff7f50',
	label = test['region'][8])

ax.set_ylabel('PageView')
ax.set_title('PageView against Campaign Type')
ax.set_xticks([p + 1.5 * width for p in pos])
ax.set_xticklabels(test['region'])
plt.xlim(min(pos)-width, max(pos)+width*8)
plt.ylim([0, max(test['3rd party literature']+
	test['academic frontier']+
	test['g-brand']+
	test['campaign_type']+
	test['g-lecture']+
	test['g-link']+
	test['g-seminar']+
	test['g-video']+
	test['g-webinar']+
	test['ime']
	)])

plt.legend(['3rd party literature','academic frontier','g-brand','campaign_type',
	'g-lecture','g-link','g-seminar','g-video','g-webinar','ime'])

plt.grid()

plt.show()


# Multiple regression # 
from statsmodels.formula.api import ols
m = ols("PV_Visit_Ratio ~ C(Int_Segment) + C(DEPARTMENT) + C(REGION) + C(EDM_Clicked) + CALL_COUNT + KM_COUNT + AVG_CALL_DURATION + AVG_PG_DURATION", DCR_iDA_Portal_Perf).fit()
print(m.summary())

ols_output = m.summary().as_text()
f = open("ols_summary.txt", "w")
f.write(ols_output)
f.close()

# COLUMN SELECTING # 
CALL = WORKCALL[Workcall_Metrics]

# DOCUMENT SELECTING #
CALL_SUB = CALL[CALL.DOCU_ID.isin(DOCU_LIST)] # returning all calls detailing the chosen materials
CALL_SUB_VALID = CALL_SUB[CALL_SUB.ISVALIDCALL == 1] # keeping valid calls only
len(CALL_SUB_VALID.index) # Number of unique calls detailing the chosen materials

# FEEDBACK TABLE GENERATION #
FB = WORKFEEDBACK[WORKFEEDBACK.DOCU_ID.isin(DOCU_LIST)][FB_Table_Metrics]
FB.columns = ['FB_ID','CALL_ID','PAGEINDEX','KM_ID','KEYMESSAGE','PAGE_DURATION','LEVEL'] # PAGE_DURATION is only meaningful to pages receiving feedback
FB_VALID = CALL_SUB_VALID.merge(FB, on = 'CALL_ID', how = 'inner') # keeping valid call ID only
FB_VALID['MONTH'] = FB_VALID.CALL_STARTDATE.map(lambda x: x.strftime('%Y-%m')) # Calendar month computation

# ADDING PAGE INFO # 
DOCU = MATERIAL[DOCU_Metrics] # Brand has been set to Seretide Asthma
DOCU.columns = ['DOCU_ID','DOCU_NAME','PAGE_NO','PAGE_TITLE']
FB_Table = FB_VALID.merge(DOCU, how = 'left', left_on = ['DOCU_ID', 'PAGEINDEX'], right_on = ['DOCU_ID', 'PAGE_NO'])
FB_Table = FB_Table.merge(REGION, how = 'left', left_on = 'PROVINCE_NAME', right_on = 'PROVINCE')

# DATA EXPORT # 
writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Feedback_Table.xlsx'))
FB_Table.to_excel(writer, 'Sheet1')
writer.save()

# CALL TABLE #
CT_PREP = FB_Table.groupby('CALL_ID')
	# For each unique call, compute metrics on pages viewed
DURA_CT = CT_PREP['PAGE_DURATION']
funcs = [
		('AVG_PG_DURATION','mean'),  
		('MEDIAN_PG_DURATION','median'),
		('MAX_PG_DURATION','max'), 
		('MIN_PG_DURATION','min'), 
		('SUM_PG_DURATION','sum'),
		('VAR_PG_DURATION','var')
		]
CT_P1 = DURA_CT.agg(funcs)
CT_P1_df = pd.DataFrame(CT_P1)
CT_P1_df.reset_index(inplace = True)

	# for each unique call, compute number of unique Key Messages viewed
KM_CT = CT_PREP['KM_ID']
CT_P2 = KM_CT.apply(lambda x: len(x.unique()))
CT_P2_df = pd.DataFrame(CT_P2)
CT_P2_df.reset_index(inplace = True)
CT_P2_df.columns = ['CALL_ID','KM_COUNT'] 

	# for each unique call, compute number of unique pages(titles) viewed
TITLE_CT = CT_PREP['PAGE_TITLE']
CT_P3 = TITLE_CT.apply(lambda x: len(x.unique()))
CT_P3_df = pd.DataFrame(CT_P3)
CT_P3_df.reset_index(inplace = True)

Call_M1 = CT_P1_df.merge(CT_P2_df, on = 'CALL_ID')
Call_M2 = Call_M1.merge(CT_P3_df, on = 'CALL_ID')
Call_Time = FB_Table[['CALL_ID','MONTH']].drop_duplicates()
Call_Table = Call_M2.merge(Call_Time, on = 'CALL_ID', how = 'left')
	# for each unique call, compute KM/Title ratio
Call_Table['KM_TITLE_RATIO'] = Call_Table['KM_COUNT']/Call_Table['PAGE_TITLE']
# DATA EXPORT #
writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Call_Table.xlsx'))
Call_Table.to_excel(writer, 'Sheet1')
writer.save()

# DOCTOR TABLE #
DT_PREP = FB_Table.groupby('DOCTOR_ID')
	# for each unique physician, compute metrics (s) on pages viewed #
DURA_DT_1 = DT_PREP['PAGE_DURATION']
DT_P1 = DURA_DT_1.agg(funcs)
DT_P1_df = pd.DataFrame(DT_P1)
DT_P1_df.reset_index(inplace = True)
	# for each unique physician, compute metrics (s) on each call #
DURA_DT_2 = DT_PREP['DURATION']
funcs_call = [
			('AVG_CALL_DURATION', 'mean'),
			('MEDIAN_CALL_DURATION', 'median'),
			('MAX_CALL_DURATION', 'max'),
			('MIN_CALL_DURATION','min'),
			('SUM_CALL_DURATION','sum'),
			('VAR_CALL_DURATION','var')
			]
DT_P2 = DURA_DT_2.agg(funcs_call)
DT_P2_df = pd.DataFrame(DT_P2)
DT_P2_df.reset_index(inplace = True)
	# for each unique physician, compute their first and last visit time #
CALL_TIME = DT_PREP['CALL_STARTDATE']
funcs_call_time = [
				('FIRST_CALL','min'),
				('LAST_CALL','max')
				]
DT_P3 = CALL_TIME.agg(funcs_call_time)
DT_P3_df = pd.DataFrame(DT_P3)
DT_P3_df.reset_index(inplace = True)
	# for each unique physician, count their total calls #
DT_P4 = DT_PREP['CALL_ID'].apply(lambda x: len(x.unique()))
DT_P4_df = pd.DataFrame(DT_P4)
DT_P4_df.reset_index(inplace = True)
DT_P4_df.columns = ['DOCTOR_ID','CALL_COUNT']
	# KM/CALL RATIO #
DT_P5 = DT_PREP['KM_ID'].apply(lambda x: len(x.unique()))
DT_P5_df = pd.DataFrame(DT_P5)
DT_P5_df.reset_index(inplace = True)
DT_P5_df.columns = ['DOCTOR_ID','KM_COUNT']
DT_P6 = DT_PREP['KEYMESSAGE'].apply(lambda x: x.isnull()) # flag null KM
DT_P5_df['KM_CONTAINS_NULL'] = DT_P6
DT_P5_df['KM_COUNT_VALID'] = np.where(DT_P5_df['KM_CONTAINS_NULL'] == True, (DT_P5_df['KM_COUNT'] - 1), DT_P5_df['KM_COUNT'])
	# Assign region to each unique physician #
DT_REGION = FB_Table[['DOCTOR_ID', 'REGION']].drop_duplicates()
	# Assign department #
DT_DEPT = FB_Table[['DOCTOR_ID', 'DEPARTMENT']].drop_duplicates()
	# Assign segment #
DT_SEGMENT = FB_Table[['DOCTOR_ID', 'DOCTOR_NATIONAL_SEGMENT']].drop_duplicates()

# DOCTOR TABLE #
Doctor_Table = DT_P1_df.merge(DT_P2_df, on='DOCTOR_ID').merge(DT_P3_df, on='DOCTOR_ID').merge(DT_P4_df, on='DOCTOR_ID').merge(DT_P5_df, on='DOCTOR_ID').merge(DT_REGION, on = 'DOCTOR_ID').merge(DT_DEPT, on = 'DOCTOR_ID').merge(DT_SEGMENT, on = 'DOCTOR_ID')
Doctor_Table['KM_CALL_RATIO'] = Doctor_Table['KM_COUNT_VALID']/Doctor_Table['CALL_COUNT']

# Data recoding #
OldNewMap = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'N': 5, 'KDM': 5}
Doctor_Table['Int_Segment'] = Doctor_Table['DOCTOR_NATIONAL_SEGMENT'].map(OldNewMap).astype(int)
FB_Table['Int_Segment'] = FB_Table['DOCTOR_NATIONAL_SEGMENT'].map(OldNewMap).astype(int)

writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Doctor_Table.xlsx'))
Doctor_Table.to_excel(writer, 'Sheet1')
writer.save()

# Call Performance # 
	# group by doctor type and department #
	# count total amount of physicians in each combination of department and national segment # 
CP_PREP = Doctor_Table.groupby(['Int_Segment','DEPARTMENT'])
CP_1 = CP_PREP['DOCTOR_ID'].apply(lambda x: len(x.unique()))
CP_1_df = pd.DataFrame(CP_1)
CP_1_df.reset_index(inplace = True)
CP_1_df.columns = ['Int_Segment','DEPARTMENT','Doctors_Total']

	# count total calls in each segment combination #
CP_2 = CP_PREP['CALL_COUNT'].agg(['sum','mean'])
CP_2_df = pd.DataFrame(CP_2)
CP_2_df.reset_index(inplace = True)
CP_2_df.columns = ['Int_Segment','DEPARTMENT','Calls_Total','Calls_Avg']

	# average KM count in each segment combo #
CP_3 = CP_PREP['KM_COUNT'].agg(['sum','mean'])
CP_3_df = pd.DataFrame(CP_3)
CP_3_df.reset_index(inplace = True)
CP_3_df.columns = ['Int_Segment','DEPARTMENT','KMs_Total','KMs_Avg']

Call_Performance = CP_1_df.merge(CP_2_df, on = ['Int_Segment', 'DEPARTMENT']).merge(CP_3_df, on = ['Int_Segment', 'DEPARTMENT'])

writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Call_Performance.xlsx'))
Call_Performance.to_excel(writer, 'Sheet1')
writer.save()

# Call Performance by month # 
	# group by doctor type and department and month #
CPM_PREP = FB_Table.groupby(['MONTH','Int_Segment','DEPARTMENT','REGION'])
CPM_1 = CPM_PREP['DOCTOR_ID'].apply(lambda x: len(x.unique()))
CPM_1_df = pd.DataFrame(CPM_1)
CPM_1_df.reset_index(inplace = True)
CPM_1_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Doctors_Total']

	# total amount of unique calls in each segment combo by month
CPM_2 = CPM_PREP['CALL_ID'].apply(lambda x: len(x.unique()))
CPM_2_df = pd.DataFrame(CPM_2
CPM_2_df.reset_index(inplace = True)
CPM_2_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Calls_Total']

	# Positive feedback in each segment combo by month
CPM_3_pos = CPM_PREP['LEVEL' == 'A'].LEVEL.apply('count') # LEVEL = 1
CPM_3_pos_df = pd.DataFrame(CPM_3_pos)
CPM_3_pos_df.reset_index(inplace = True)
CPM_3_pos_df.columns = ['MONTH','Int_Segment','DEPARTMENT','POSITIVE']

CPM_3_neu = CPM_PREP['LEVEL'].apply(lambda x: len(x == 'B')) # LEVEL = 2
CPM_3_neu_df = pd.DataFrame(CPM_3_neu)
CPM_3_neu_df.reset_index(inplace = True)
CPM_3_neu_df.columns = ['MONTH','Int_Segment','DEPARTMENT','NEUTRAL']

CPM_3_neg = CPM_PREP['LEVEL'].apply(lambda x: len(x == 'C')) # LEVEL = 3
CPM_3_neg_df = pd.DataFrame(CPM_3_neg)
CPM_3_neg_df.reset_index(inplace = True)
CPM_3_neg_df.columns = ['MONTH','Int_Segment','DEPARTMENT','NEGATIVE']

	# Unique Key message in each segment combo by month #
CPM_4 = CPM_PREP['KEYMESSAGE'].apply(lambda x: len(x.unique()))
CPM_4_df = pd.DataFrame(CPM_4)
CPM_4_df.reset_index(inplace = True)
CPM_4_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Unique_KMs']

	# Average call duration in each segment combo by month #
CPM_5 = CPM_PREP['DURATION'].agg('mean')
CPM_5_df = pd.DataFrame(CPM_5)
CPM_5_df.reset_index(inplace = True)
CPM_5_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Call_Duration_Avg']

	# Total pages viewed in each segment combo by month #
CPM_6 = CPM_PREP['PAGE_TITLE'].agg('count')
CPM_6_df = pd.DataFrame(CPM_6)
CPM_6_df.reset_index(inplace = True)
CPM_6_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Pages_Count']

	# Unique pages viewed in each segment by month #
CPM_7 = CPM_PREP['PAGE_TITLE'].apply(lambda x: len(x.unique()))
CPM_7_df = pd.DataFrame(CPM_7)
CPM_7_df.reset_index(inplace = True)
CPM_7_df.columns = ['MONTH','Int_Segment','DEPARTMENT','REGION','Unique_Pages_Count']

CPM = [CPM_1_df, CPM_2_df, CPM_4_df, CPM_5_df, CPM_6_df, CPM_7_df]
current = CPM[0]
for i, frame in enumerate(CPM[1:], 2):
	current = current.merge(frame, on=['MONTH','Int_Segment','DEPARTMENT','REGION'])

writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Call_Performance_by_Month.xlsx'))
current.to_excel(writer, 'Sheet1')
writer.save()

# Adding page title classification #
title_classification = pd.read_excel(os.path.join(Root_Dir, In, 'classification.xlsx'))
FB_Table = FB_Table.merge(title_classification, left_on = 'PAGE_TITLE', right_on = 'Title', how = 'left')
TITLE_PREP = FB_Table.groupby(['Tag','MONTH','Int_Segment','DEPARTMENT','REGION'])

	# count total number of physicians #
T_1 = TITLE_PREP['DOCTOR_ID'].apply(lambda x: len(x.unique()))
T_1_df = pd.DataFrame(T_1)
T_1_df.reset_index(inplace = True)
T_1_df.columns = ['Tag','MONTH','Int_Segment','DEPARTMENT','REGION','Doctors_Total']
	
	# count total call duration # 
T_2 = TITLE_PREP['DURATION'].agg('sum')
T_2_df = pd.DataFrame(T_2)
T_2_df.reset_index(inplace = True)
T_2_df.columns = ['Tag','MONTH','Int_Segment','DEPARTMENT','REGION','Total_Call_Duration']

	# count average page view duration 
T_3 = TITLE_PREP['PAGE_DURATION'].agg('mean')
T_3_df = pd.DataFrame(T_3)
T_3_df.reset_index(inplace = True)
T_3_df.columns = ['Tag','MONTH','Int_Segment','DEPARTMENT','REGION','PAGE_DURATION_Avg']

	# count unique page view for each tag #
T_4 = TITLE_PREP['Title'].agg('count')
T_4_df = pd.DataFrame(T_4)
T_4_df.reset_index(inplace = True)
T_4_df.columns = ['Tag','MONTH','Int_Segment','DEPARTMENT','REGION','Total_PV']

T_list = [T_1_df, T_2_df, T_3_df, T_4_df]
T_current = T_list[0]
for i, frame in enumerate(T_list[1:], 2):
	T_current = T_current.merge(frame, on = ['Tag','MONTH','Int_Segment','DEPARTMENT','REGION'])

writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'Title_Performance.xlsx'))
T_current.to_excel(writer, 'Sheet1')
writer.save()


# Doctor ID Matching: iDA & Portal #
iDA_DCR_UNIQUE = pd.Series(Doctor_Table.DOCTOR_ID)
PORTAL_DCR_UNIQUE = pd.Series(ACTIVE_DCR_PORTAL_UNIQUE)
iDA_PORTAL_DCR = list(set(iDA_DCR_UNIQUE) & (set(PORTAL_DCR_UNIQUE)))
Doctor_Table['MULTI_CHANNEL'] = 1 if Doctor_Table.DOCTOR_ID.isin(iDA_PORTAL_DCR) else 0

MULTI_CHANNEL_DCR = Doctor_Table[Doctor_Table.DOCTOR_ID.isin(iDA_PORTAL_DCR)]
iDA_ONLY_DCR = Doctor_Table[-Doctor_Table.DOCTOR_ID.isin(iDA_PORTAL_DCR)] # Doctors that are only active on iDA
# Drop trivial departments, keep 呼吸科，儿科 only
MULTI_CHANNEL_DCR_RESP = MULTI_CHANNEL_DCR[MULTI_CHANNEL_DCR.DEPARTMENT.isin(['呼吸科'])]
MULTI_CHANNEL_DCR_PEDIATRICS = MULTI_CHANNEL_DCR[MULTI_CHANNEL_DCR.DEPARTMENT.isin(['儿科'])]
# Get the echoing subset for iDA-only DCRs
iDA_ONLY_DCR_RESP = iDA_ONLY_DCR[iDA_ONLY_DCR.DEPARTMENT.isin(['呼吸科'])]
iDA_ONLY_DCR_PEDIATRICS = iDA_ONLY_DCR[iDA_ONLY_DCR.DEPARTMENT.isin(['儿科'])]

# distribution (to be functioned)
d1_region = iDA_ONLY_DCR_RESP['REGION'].value_counts()
d1_region = pd.DataFrame(d1_region)
d1_region['region'] = d1_region.index.tolist()

d2_region = MULTI_CHANNEL_DCR_RESP.REGION.value_counts()
d2_region = pd.DataFrame(d2_region)
d2_region['region'] = d2_region.index.tolist()

d1_segment = iDA_ONLY_DCR_RESP['Int_Segment'].value_counts()
d1_segment = pd.DataFrame(d1_segment)
d1_segment['segment'] = d1_segment.index.tolist()

d2_segment = MULTI_CHANNEL_DCR_RESP['Int_Segment'].value_counts()
d2_segment = pd.DataFrame(d2_segment)
d2_segment['segment'] = d2_segment.index.tolist()

# Call on: iDA-only doctors & portal doctors
CT_2 = Call_Table.merge(FB_Table[['CALL_ID','DOCTOR_ID']].drop_duplicates(), how = 'left')
iDA_ONLY_DCR_Call = CT_2[-CT_2.DOCTOR_ID.isin(iDA_PORTAL_DCR)]
MULTI_CHANNEL_DCR_Call = CT_2[CT_2.DOCTOR_ID.isin(iDA_PORTAL_DCR)]




# bulk export
list_dfs = [d1_region, d1_segment, d2_region, d2_segment, iDA_ONLY_DCR, MULTI_CHANNEL_DCR, iDA_ONLY_DCR_Call, MULTI_CHANNEL_DCR_Call]
writer = pd.ExcelWriter(os.path.join(Root_Dir, Out, 'iDA_Multi.xlsx'))
for n, df in enumerate(list_dfs):
    df.to_excel(writer, 'Sheet%s' % n)
writer.save()





# Statistical analysis
gb_national_segment = Doctor_Table.groupby('Int_Segment')
for segment, value in gb_national_segment['CALL_COUNT']:
	print((segment, value.mean()))
gb_national_segment.mean() # returning mean values for all variables (regardless of whether it's numerical or categorical)

# OLS
from scipy import stats
stats.ttest_1samp(Doctor_Table['CALL_COUNT'], 0)
from statsmodels.formula.api import ols





	# Title: by Month #
params = [Title_Sub.Tag, Title_Sub.MONTH]
T2 = Title_Sub.groupby(params)
DURA_2 = T2['DURATION']
R2 = DURA_2.agg(funcs)
R2_df = pd.DataFrame(R2)
R2_df.reset_index(inplace = True) # Long table
R2_reshaped = R2_df.pivot(index = 'MONTH', columns = 'Tag', values = 'mean') # wide table
R2_reshaped.reset_index(inplace = True)


	# Title: by MONTH & Department #
params = [Title_Sub.Tag, Title_Sub.MONTH, Title_Sub.DEPARTMENT]
T3 = Title_Sub.groupby(params)
DURA_3 = T3['DURATION']
R3 = DURA_3.agg(funcs)
R3_df = pd.DataFrame(R3)
R3_df.reset_index(inplace = True)
R3_reshaped = R3_df.pivot_table(values = 'mean', index = ['MONTH','DEPARTMENT'], columns = 'Tag')
R3_reshaped.reset_index(inplace = True)


	# Title: by Department #
params = [Title_Sub.Tag, Title_Sub.DEPARTMENT]
T4 = Title_Sub.groupby(params, as_index = False)
DURA_4 = T4['DURATION']
R4 = DURA_4.agg(funcs)
R4_df = pd.DataFrame(R4)
R4_reshaped = R4_df.pivot_table(values = 'mean', index = 'DEPARTMENT', columns = 'Tag')













