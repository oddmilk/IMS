'''

Information Extraction 
@author: Oddmilk

'''

####################################################################################################
# Load packages 

import os
import pandas as pd
import numpy as np
import re
from pandas import ExcelWriter

# Set working directory
path = os.getcwd()
files = os.listdir(path)
# Pick out files of interest
files_xlsx = [f for f in files if f[-4:] == 'xlsx'] 
# Initialize empty dataframe
raw = pd.DataFrame()
# Loop over list of excel files to append to the empty dataframe
for f in files_xlsx:
  data = pd.read_excel(f, 'Sheet1')
  raw = raw.append(data)


# Find physicians with identical names working in the same hospital and same department #
test = raw[['hospital','dept','doctor','data_source']]
t1 = test.loc[test['data_source'] != '好大夫']
dl1 = t1[['hospital','dept','doctor']].duplicated(keep = False) # 1719

t2 = test.loc[test['data_source'] != '挂号网']
dl2 = t2[['hospital','dept','doctor']].duplicated(keep = False)

t3 = test.loc[test['data_source'] != '丁香园']
dl3 = t3[['hospital','dept','doctor']].duplicated(keep = False)

dl4 = test[['hospital','dept','doctor']].duplicated(keep = False)



##############################
# Split data into three sets #
##############################
  # Hospital
fields_hco = ['data_source', 'province', 'city', 'hospital', 'hospital_level', 'hospital_url', 'hospital_phone', 'hospital_address', 'hospital_synopsis']
hco = raw[fields_hco].drop_duplicates().reset_index(drop = True)
  # Department
fields_dept = ['data_source', 'hospital', 'dept', 'dept_url', 'dept_synopsis']
dept = raw[fields_dept].drop_duplicates().reset_index(drop = True)
  # Physician
fields_dcr = ['data_source', 'hospital', 'dept', 'doctor', 'doctor_url', 'doctor_position', 'doctor_skill', 'doctor_synopsis']
dcr = raw[fields_dcr].reset_index(drop = True)

#############################
###### Hospital level #######
#############################

# Keep sentences that have numeric values
alphanumeric_pat = re.compile("(\w*\d+\w*)")
hco['synopsis_s'] = hco.hospital_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))

	# Number of beds #
hco['beds'] = hco.hospital_synopsis.apply(lambda x: bedNum(x))
hco['beds'] = hco.beds.apply(lambda x: firstFound(x))
	# Number of outpatients #
hco['outpatients'] = hco.hospital_synopsis.apply(lambda x: outPatient(x))
hco['outpatients'] = hco.outpatients.apply(lambda x: firstFound(x))

  # Number of inpatients # 
hco['inpatients'] = hco.hospital_synopsis.apply(lambda x: inPatient(x))
hco['inpatients'] = hco.inpatients.apply(lambda x: firstFound(x))

hco['inpatients2'] = hco.hospital_synopsis.apply(lambda x: inPatient2(x))
hco['inpatients2'] = hco.inpatients2.apply(lambda x: firstFound(x))

hco['inpatients3'] = hco.hospital_synopsis.apply(lambda x: inPatient3(x))
hco['inpatients3'] = hco.inpatients3.apply(lambda x: firstFound(x))

	# Number of surgeries # 
hco['surgeries'] = hco.hospital_synopsis.apply(lambda x: surgeries(x))
hco['surgeries'] = hco.surgeries.apply(lambda x: firstFound(x))  # partial success. # 台手术is missing

# Extraction assessment
hco_grp = hco.groupby('data_source')
# hospital output assessment
hco_grp[hco.columns[1:]].count()


########################################
##### Department level 
########################################
dept['synopsis_s'] = dept.dept_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))
	# Number of beds #
dept['beds'] = dept.dept_synopsis.apply(lambda x: bedNum(x)).apply(lambda x: firstFound(x))

	# Number of outpatients #
dept['outpatients'] = dept.dept_synopsis.apply(lambda x: outPatient(x)).apply(lambda x: firstFound(x))
	# Number of inpatients #
dept['inpatients'] = dept.dept_synopsis.apply(lambda x: inPatient(x)).apply(lambda x: firstFound(x))

	# Number of surgeries #
dept['surgeries'] = dept.dept_synopsis.apply(lambda x: surgeries(x)).apply(lambda x: maxElement(x))  # need to deal with NoneType


	# Number of 主任医师 | 副主任医师 | 住院医师 | 主治医师 | 博士 | 硕士 #
dept['chief'] = dept.dept_synopsis.apply(lambda x: deptChief(x)).apply(lambda x: firstFound(x))
dept['ViceChief'] = dept.dept_synopsis.apply(lambda x: deptViceChief(x)).apply(lambda x: firstFound(x))
dept['Resident'] = dept.dept_synopsis.apply(lambda x: deptResident(x)).apply(lambda x: firstFound(x))
dept['Attending'] = dept.dept_synopsis.apply(lambda x: deptAttending(x)).apply(lambda x: firstFound(x))
dept['Nurse'] = dept.dept_synopsis.apply(lambda x: deptNurse(x)).apply(lambda x: firstFound(x))

dept_grp = dept.groupby('data_source')
dept_grp[dept.columns[1:]].count()


########################################
##### Physician level 
########################################
dcr['doctor_synopsis_shortened'] = dcr.doctor_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))

dcr['gender'] = dcr.doctor_synopsis.apply(lambda x: dcrGender(x)).apply(lambda x: firstFound(x))
  # is_PHD
dcr['is_Phd'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '博士'))
  # is_master
dcr['is_ms'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '硕士'))
  # has_publication 发表
dcr['has_publication'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '论文'))
  # is_mentor 导师
dcr['is_mentor'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '导师'))
  # is_involved_in_clinical_trial 临床试验，新药，试验
dcr['is_involved_in_clinical_trial'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '临床试验|新药|试验'))
  # is_retired 退休
dcr['is_retired'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '退休'))
  # is_public_speaker
dcr['is_public_speaker'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '讲座'))
  # is_royal_society_member
dcr['membership'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '学会会员|委员'))
  # study_abroad
dcr['study_abroad'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '留学'))
  # patent
dcr['patent'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '专利'))  
  # school: undergrad 
dcr['school'] = dcr.doctor_synopsis.apply(lambda x: grad(x)).apply(lambda x: firstFound(x))
  # school: grad / phd (to be done)
dcr['grad_1'] = dcr.doctor_synopsis.apply(lambda x: grad(x)).apply(lambda x: secondFound(x))

  # expertise in: 不孕不育; 妇产科护理;泌尿疾病
dcr['sterile'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '不孕不育'))
dcr['digestion'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '肠胃'))
dcr['digestion_2'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '消化'))
dcr['urinary'] = dcr.doctor_synopsis.apply(lambda x: exist(x, '泌尿'))



synopsis_extract_list = [hco, dept, dcr]
save_xls(synopsis_extract_list, 'synopsis_extract.xlsx')

# 眼科
d0 = dcr.loc[dcr.dept.str.contains('眼科', na = False)]

# 眼底病
d1 = d0[d0['doctor_skill'].str.contains('眼底病', na = False)]
d2 = d0[d0['doctor_synopsis'].str.contains('眼底病', na = False)]
d3 = d1.append(d2).drop_duplicates()
writer = ExcelWriter('ophthalmology.xlsx')
d3.to_excel(writer, 'Sheet1')
writer.save()

# dcr with an expertise in 不孕不育
d4 = dcr[dcr.doctor_skill.str.contains('不孕不育', na = False)]
d5 = dcr[dcr.doctor_synopsis.str.contains('不孕不育', na = False)]
d5 = d4.append(d5).drop_duplicates()
writer = ExcelWriter('sterile.xlsx')
d5.to_excel(writer, 'Sheet1')
writer.save()

len(d5)
len(d5.hospital.unique())
len(d5.groupby(['hospital','dept']).count())

# dcr with an expertise in 泌尿
d6 = dcr[dcr.doctor_skill.str.contains('泌尿', na = False)]
d7 = dcr[dcr.doctor_synopsis.str.contains('泌尿', na = False)]
d8 = d6.append(d7).drop_duplicates()
writer = ExcelWriter('urinary.xlsx')
d8.to_excel(writer, 'Sheet1')
writer.save()

len(d8)
len(d8.hospital.unique())
len(d8.groupby(['hospital','dept']).count())

# dcr with an expertise in 消化科／肠胃
d9 = dcr[dcr.doctor_skill.str.contains('消化', na = False)]
d10 = dcr[dcr.doctor_synopsis.str.contains('消化', na = False)]
d11 = d9.append(d10).drop_duplicates()
writer = ExcelWriter('digestion.xlsx')
d11.to_excel(writer, 'Sheet1')
writer.save()

len(d11)
len(d11.hospital.unique())
len(d11.groupby(['hospital','dept']).count())

# 夜尿症
d12 = dcr[dcr.doctor_skill.str.contains('夜尿', na = False)]
d13 = dcr[dcr.doctor_synopsis.str.contains('夜尿', na = False)]
d14 = d12.append(d13).drop_duplicates()
writer = ExcelWriter('nocturia.xlsx')
d14.to_excel(writer, 'Sheet1')
writer.save()

len(d14)
len(d14.hospital.unique())
len(d14.groupby(['hospital','dept']).count())

# 肠胃疾病
d15 = dcr[dcr.doctor_skill.str.contains('肠胃', na = False)]
d16 = dcr[dcr.doctor_synopsis.str.contains('肠胃', na = False)]
d17 = d15.append(d16).drop_duplicates()
writer = ExcelWriter('gastro.xlsx')
d17.to_excel(writer, 'Sheet1')
writer.save()

len(d17)
len(d17.hospital.unique())
len(d17.groupby(['hospital','dept']).count())

# 推迟早产
d18 = dcr[dcr.doctor_skill.str.contains('早产', na = False)]
d19 = dcr[dcr.doctor_synopsis.str.contains('早产', na = False)]
d20 = d18.append(d19).drop_duplicates()
writer = ExcelWriter('早产.xlsx')
d20.to_excel(writer, 'Sheet1')
writer.save()

len(d20)
len(d20.hospital.unique())
len(d20.groupby(['hospital','dept']).count())


# Strip end-of-line terminators (\r\n)
ghw.hospital = ghw.hospital.str.strip() 





