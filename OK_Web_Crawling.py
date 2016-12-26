# Load required packages
import os
import pandas as pd
import numpy as np
import re



# Use converters to remove extra whitespace when parsing the file (to be moved to information_extraction file)
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


# Keep characters that have numeric values only
def numExtraction(var, pat):
  if isinstance(var, float):
    return None
  else:
#    var = re.sub('、',',',var)
    var = re.sub('[\s+]', '', var)
    var = var.strip()
    tmp = re.findall(pat, var)
    return ','.join(tmp)


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

def firstFound(text):
  if isinstance(text,float):
    pass  
  else:
    return first(text)

# Select the second element # 
def second(text):
  if len(text) >= 2:
      return text[1]
  else:
    return None

def secondFound(text):
  if isinstance(text,float):
    pass  
  else:
    return second(text)



# Select the element with max length
def maxElement(text):
  a = []
  if isinstance(text,float):
    pass
  elif text == a:
    pass
  else:
    return max(list(text), key = len)




try:
    found = re.findall("手术(.+?例)?，|手术(.+?例)?。|手术(.+?例)?；", text)
except AttributeError:
    found = '' # apply your error handling


def outPatient(text):
    try:
        return re.findall("年?月?日?门急?诊量\w+\d+\w+人次?", text)
    except TypeError:
        return text

def outPatient1(text):
    try:
        return re.findall("年?月?日?门急?诊量(\w+\d+\w+人次?)，", text)
    except TypeError:
        return text


def inPatient(text):
    try:
        return re.findall("出院(\w+\d+多?余?人次?)|收治(\w+\d+多?余?人次?)|住院病人(\w+\d+多?余?人次?)", text)
    except TypeError:
        return text


def surgeries(text):
    try:
        return re.findall('(手术量?数?\w+?台)，?|(手术\w+?例)，?', text)
    except TypeError:
        return text

def surgeries2(text):
    try:
        return re.findall('(手术\w+?例)，?' , text)
    except TypeError:
        return ''


# calculate the sum of all surgeries if there are multiple finds #
def calcSurgeries(text):
    if isinstance(text, float):
      pass
    else: 
      return calc(text)

def deptChief(text):
    try:
        return re.findall('主任医师(\d+)人', text)
    except TypeError:
        return text  

def deptViceChief(text):
    try:
        return re.findall('副主任医师(\d+)人', text)
    except TypeError:
        return text  

def deptResident(text):
    try:
        return re.findall('住院医师(\d+)人', text)
    except TypeError:
        return text

def deptAttending(text):
    try:
        return re.findall('主治医师(\d+)人', text)
    except TypeError:
        return text

def deptNurse(text):
    try:
        return re.findall('护士(\d+)人', text)
    except TypeError:
        return text

def dcrGender(text):
    try:
        return re.findall('男|女', text)
    except TypeError:
        return text

### function extracting information at individual level ###
def grad(text):
    if str(text) == 'nan':
       return text
    else: 
       m = re.search('毕业于', text)
       n = re.search('毕业，', text)
       if m is None: 
          return re.findall('(\w+)毕业\w+，', text)
       else: 
          return re.findall('毕业于(\w+)', text)

def exist(text, keyword):
    if isinstance(text, float):
        pass
    elif re.search(keyword, text):
        return 1
    else:
        return 0

# bulk export data to excel #
from pandas import ExcelWriter

def save_xls(list_dfs, xls_path):
    writer = pd.ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()


import os
import math

# create a new path for files 
def make_dirs(path):
  if not os.path.isdir(path):
    os.makedirs(path)

# obtain the total number of lines in a file
def get_total_lines(filepath):
  if not os.path.exists(filepath):
    return 0
  cmd = 'wc -l %s' % filepath  # wc: word count
  return int(os.popen(cmd).read().split()[0])



ghw = pd.read_excel("/Users/mengjichen/Desktop/POC/ghw.xlsx", sep=r'',
                      names=["data_source", "province", "city", 
                          "hospital", "hospital_url", "hospital_synopsis", "hospital_phone", "hospital_address",
                          "dept", "dept_url", "dept_synopsis", 
                          "doctor", "doctor_url", "doctor_synopsis", "doctor_skill", "doctor_position", "hospital_level"],
                      converters = {'hospital' : strip
                                    })





































