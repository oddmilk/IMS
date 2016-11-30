# README #
## This python sript is prepared for data extraction from text files ##
## 

# OK web crawling #
import os
import pandas as pd
import numpy as np
import re

root_dir = '/Users/mengjichen/Desktop/'
here = 'sample.xlsx'
filepath = os.path.join(root_dir, here)

dxy = pd.read_csv('丁香园.csv')
hdf = pd.read_csv('好大夫.csv')
ghw = pd.read_csv('挂号网.csv')


# Use converters to remove extra whitespace when parsing the file (to be moved to information_extraction file)
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


hospital_main = pd.read_excel("/Users/mengjichen/Desktop/POC/hdf.xlsx", sep=r'',
                      names=["id", "data_source", "province", "city", 
                      		"hospital", "hospital_url", "hospital_synopsis", "hospital_phone", "hospital_address",
                      		"dept", "dept_url", "dept_synopsis", 
                      		"doctor", "doctor_url", "doctor_synopsis", "doctor_skill", "doctor_position", "hospital_level"],
                      converters = {'hospital_synopsis' : strip,
                                    'dept_synopsis' : strip,
                                    'doctor_synopsis' : strip
                                    })

hco_synopsis = hospital_main[["hospital", "hospital_synopsis"]].drop_duplicates().reset_index(drop = True)
dept_synopsis = hospital_main[["hospital", "dept", "dept_synopsis"]].drop_duplicates().reset_index(drop = True)
doctor_synopsis = hospital_main[["id", "doctor", "doctor_synopsis"]]


### 对所有简介类字段，将所有中文符号改成英文符号 ###
def punctuationConverter(s):
  re.sub('，', ',', s)
  re.sub('。', '.', s)
  re.sub('：', ':', s)


# functions extracting information at hospital level # 
def bedNum(text):
    try:
        return re.findall("(\d+)余?张", text)
    except TypeError:
        return text

# Select the first element # 
def first(text):
  if len(text) >= 1:
      return text[0]
  else:
    return None

# Return the first found pattern 
def firstFound(text):
  if isinstance(text,float):
    pass  
  else:
    return first(text)

def outPatient(text):
    try:
        return re.findall("年?月?日?门急?诊量\w+\d+\w+人次", text)
    except TypeError:
        return text


def inPatient(text):
    try:
        return re.findall("住院(\w+\d+)多?人次", text)
    except TypeError:
        return text

def surgeries(text):
    try:
        return re.findall('(\w+\d+余?例)', text)
    except TypeError:
        return text

def deptChief(text):
    try:
        return re.findall('主任医师(\d+)人', text)
    except TypeError:
        return text  

def deptSousChief(text):
    try:
        return re.findall('副主任医师(\d+)人', text)
    except TypeError:
        return text  

def deptResident(text):
    try:
        return re.findall('住院医师(\d+)人', text)
    except TypeError:
        return text

def dcrGender(text):
    try:
        return re.findall('男|女', text)
    except TypeError:
        return text

### function extracting information at individual level ###
def undergrad(text):
    if str(text) == 'nan':
       return text
    else: 
       m = re.search('毕业于', text)
       n = re.search('毕业，', text)
       if m is None: 
          return re.findall('(\w+)毕业\w+，', text)
       else: 
          return re.findall('毕业于(\w+)', text)

## function creating dummy variables including: ##
  # is_event_participant: 讲师，讲座，科普
  # has_affiliation 学会，委员会，委员，


def exist(text, keyword):
    if isinstance(text, float):
        pass
    elif re.search(keyword, text):
        return 1
    else:
        return 0




hospital_beds = []
dept_beds = []
dcr_clinical_trial = []
dcr_undergrad = []

for i in range(len(sample)):
#  x = bedNum(sample.hospital_synopsis[i])
#  y = bedNum(sample.dept_synopsis[i])
#  z = dummy(sample.doctor_synopsis[i])
  u = undergrad(sample.doctor_synopsis[i])
  dcr_undergrad.append(u)
#  hospital_beds.append(x)
#  dept_beds.append(x)
#  dcr_clinical_trial.append(z)



























