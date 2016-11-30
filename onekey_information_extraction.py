'''

Text Processing Functions
Time: 11/25/2016
@author: Vera 

'''

####################################################################################################
# Load necessary packages （eventually there will be ~10G raw data)

import pandas as pd
import numpy as np
import re
from pandas import ExcelWriter

# Data source
synopsis_hco = ['hospital', 'hospital_synopsis']
synopsis_dept = ['hospital', 'dept', 'dept_synopsis']
synopsis_dcr = ['id', 'doctor', 'doctor_synopsis']

# Load data
raw = pd.read_excel("/Users/mengjichen/Desktop/POC/hdf.xlsx", sep=r'',
                      names=["id", "data_source", "province", "city", 
                      		"hospital", "hospital_url", "hospital_synopsis", "hospital_phone", "hospital_address",
                      		"dept", "dept_url", "dept_synopsis", 
                      		"doctor", "doctor_url", "doctor_synopsis", "doctor_skill", "doctor_position", "hospital_level"],
                      converters = {'hospital_synopsis' : strip,
                                    'dept_synopsis' : strip,
                                    'doctor_synopsis' : strip
                                    })


######################################
###### Hospital level #######
######################################
raw_synopsis_hco = raw[synopsis_hco].drop_duplicates().reset_index(drop = True)

# Fields to be extracted: Number of beds, Number of inpatients, Number of outpatients #
	# Number of beds #
raw_synopsis_hco['beds'] = raw_synopsis_hco.hospital_synopsis.apply(lambda x: bedNum(x))
raw_synopsis_hco['beds'] = raw_synopsis_hco.beds.apply(lambda x: firstFound(x))
	# Number of outpatients #
raw_synopsis_hco['outpatients'] = raw_synopsis_hco.hospital_synopsis.apply(lambda x: outPatient(x))
raw_synopsis_hco['outpatients'] = raw_synopsis_hco.outpatients.apply(lambda x: firstFound(x))

	# Number of surgeries # 
raw_synopsis_hco['surgeries'] = raw_synopsis_hco.hospital_synopsis.apply(lambda x: surgeries(x))
raw_synopsis_hco['surgeries'] = raw_synopsis_hco.surgeries.apply(lambda x: firstFound(x))  # partial success. # 台手术is missing

	# Number of inpatients # 

	# Number of newborn #


########################################
##### Department level 
########################################
raw_synopsis_dept = raw[synopsis_dept].drop_duplicates().reset_index(drop = True)
	# Number of beds #
raw_synopsis_dept['dept_beds'] = raw_synopsis_dept.dept_synopsis.apply(lambda x: bedNum(x)).apply(lambda x: firstFound(x))

	# Number of outpatients #

	# Number of inpatients #

	# Number of surgeries #

	# Number of 主任医师 | 副主任医师 | 住院医师 | 主治医师 | 博士 | 硕士 #
raw_synopsis_dept['chief'] = raw_synopsis_dept.dept_synopsis.apply(lambda x: deptChief(x)).apply(lambda x: firstFound(x))
raw_synopsis_dept['Souschief'] = raw_synopsis_dept.dept_synopsis.apply(lambda x: deptSousChief(x)).apply(lambda x: firstFound(x))
raw_synopsis_dept['Resident'] = raw_synopsis_dept.dept_synopsis.apply(lambda x: deptResident(x)).apply(lambda x: firstFound(x))



########################################
##### Physician level 
########################################
raw_synopsis_dcr = raw[synopsis_dcr]
raw_synopsis_dcr['gender'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: dcrGender(x)).apply(lambda x: firstFound(x))
  # is_PHD
raw_synopsis_dcr['is_Phd'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '博士'))
  # is_master
raw_synopsis_dcr['is_ms'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '硕士'))
  # has_publication 发表
raw_synopsis_dcr['has_publication'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '论文'))
  # is_mentor 导师
raw_synopsis_dcr['is_mentor'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '导师'))
  # is_involved_in_clinical_trial 临床试验，新药，试验
raw_synopsis_dcr['is_involved_in_clinical_trial'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '临床试验|新药|试验'))
  # is_retired 退休
raw_synopsis_dcr['is_retired'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '退休'))
  # is_public_speaker
raw_synopsis_dcr['is_public_speaker'] = raw_synopsis_dcr.doctor_synopsis.apply(lambda x: exist(x, '讲座'))


# Strip end-of-line terminators (\r\n)
ghw.hospital = ghw.hospital.str.strip() 
