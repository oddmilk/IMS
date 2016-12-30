
# 将多个dataframe存储至一个excel文件中多个sheet
def save_wb(list_dfs, wb_path):
    writer = pd.ExcelWriter(wb_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    

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


# 对所有简介类字段，将所有中文符号改成英文符号 #
def punctuationConverter(s):
  re.sub('，', ',', s)
  re.sub('。', '.', s)
  re.sub('：', ':', s)


# 从医院（科室）文字简介中抓取床位数 #
def bedNum(text):
    try:
        return re.findall("(\d+)余?张", text)
    except TypeError:
        return text

# 对于有多个床位数信息的文字简介，选第一个（通常默认第二个及之后的属于breakdown的信息） #
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


# 从文字介绍中抽取门诊量 #
  # 门诊量的文字形式： #
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

# 住院量 #
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

def Chief(text):
    try:
        return re.findall('主任医师(\d+)人', text)
    except TypeError:
        return text  

def ViceChief(text):
    try:
        return re.findall('副主任医师(\d+)人', text)
    except TypeError:
        return text  

def Resident(text):
    try:
        return re.findall('住院医师(\d+)人', text)
    except TypeError:
        return text

def Attending(text):
    try:
        return re.findall('主治医师(\d+)人', text)
    except TypeError:
        return text

def Nurse(text):
    try:
        return re.findall('护士(\d+)人', text)
    except TypeError:
        return text

def PhDAdvisor(text):
    try:
        return re.findall('博士生导师(\d+)人', text)
    except TypeError:
        return text

def MasterAdvisor(text):
    try:
        return re.findall('硕士生导师(\d+)人', text)
    except TypeError:
        return text

def Expert(text):
    try:
        return re.findall('专家(\d+)人', text)
    except TypeError:
        return text

def Professor(text):
    try:
        return re.findall('教授(\d+)人', text)
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



import os
import math

# create a new path for files 
def make_dirs(path):
  if not os.path.isdir(path):
    os.makedirs(path)


def get_total_lines(filepath):
  if not os.path.exists(filepath):
    return 0
  cmd = 'wc -l %s' % filepath  # wc: word count
  return int(os.popen(cmd).read().split()[0])





































