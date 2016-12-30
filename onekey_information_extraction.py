'''

Information Extraction 
@author: Oddmilk

'''

####################################################################################################
# 加载函数包

import os
import pandas as pd
import numpy as np
import re
from pandas import ExcelWriter

# 读取当前所在路径
path = os.getcwd()
files = os.listdir(path)
# 读取所有csv格式的源文件
files_csv = [f for f in files if f[-3:] == 'csv'] 

# 对同一个源网站爬下的csv格式的数据数数
total_vol = []
for i in range(len(files_csv)):
    temp = get_total_lines(files_csv[i])
    total_vol.append(temp)


# 将csv格式的源文件读取为列表
raw_list = []

for f in files_csv:
  data = pd.read_csv(f, sep = ";")
  raw_list.append(data)

# 将源文件从csv转为xlsx格式保存
for i in range(len(raw_list)):
  filename = raw_list[i].province.unique()
  writer = pd.ExcelWriter(os.path.join(str(filename) + '.xlsx'))
  raw_list[i].to_excel(writer, 'raw')
  writer.save()



# 将数据分成三组：医院，科室，医生 #
fields_hco = ['data_source', 'province', 'city', 'hospital', 'hospital_level', 'hospital_url', 'hospital_phone', 'hospital_address', 'hospital_synopsis']   # 医院
fields_dept = ['data_source', 'hospital', 'dept', 'dept_url', 'dept_synopsis'] # 科室
fields_dcr = ['data_source', 'hospital', 'dept', 'doctor', 'doctor_url', 'doctor_position', 'doctor_skill', 'doctor_synopsis']   # 医生

dcr_list = []
dept_list = []   
hco_list = [] 

for i in range(len(raw_list)):
    hco_temp = raw_list[i][fields_hco].drop_duplicates().reset_index(drop = True)
    hco_list.append(hco_temp)
    dept_temp = raw_list[i][fields_dept].drop_duplicates().reset_index(drop = True)
    dept_list.append(dept_temp)
    dcr_temp = raw_list[i][fields_dcr].drop_duplicates().reset_index(drop = True)
    dcr_list.append(dcr_temp)



# 医院，科室 #
for i in range(len(raw_list)):
  # 带数字的内容 #
#    hco_list[i]['s'] = hco_list[i].hospital_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))
#    dept_list[i]['s'] = dept_list[i].dept_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))
  # 床位数 #
    hco_list[i]['hco_beds'] = hco_list[i].hospital_synopsis.apply(lambda x: bedNum(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_beds'] = dept_list[i].dept_synopsis.apply(lambda x: bedNum(x)).apply(lambda x: firstFound(x))
  # 门诊量 #
    hco_list[i]['hco_outpatients'] = hco_list[i].hospital_synopsis.apply(lambda x: outPatient(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_outpatients'] = dept_list[i].dept_synopsis.apply(lambda x: outPatient(x)).apply(lambda x: firstFound(x))
  # 住院量 # 
    hco_list[i]['hco_inpatients'] = hco_list[i].hospital_synopsis.apply(lambda x: inPatient(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_inpatients'] = dept_list[i].dept_synopsis.apply(lambda x: inPatient(x)).apply(lambda x: firstFound(x))
  # 手术量 # 
    hco_list[i]['hco_surgeries'] = hco_list[i].hospital_synopsis.apply(lambda x: surgeries(x)).apply(lambda x: firstFound(x)) # 台手术is missing
    dept_list[i]['dept_surgeries'] = dept_list[i].dept_synopsis.apply(lambda x: surgeries(x)).apply(lambda x: firstFound(x))
  # 主任医师 #
    hco_list[i]['hco_Chief'] = hco_list[i].hospital_synopsis.apply(lambda x: Chief(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Chief'] = dept_list[i].dept_synopsis.apply(lambda x: Chief(x)).apply(lambda x: firstFound(x))
  # 副主任医师 #
    hco_list[i]['hco_ViceChief'] = hco_list[i].hospital_synopsis.apply(lambda x: ViceChief(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_ViceChief'] = dept_list[i].dept_synopsis.apply(lambda x: ViceChief(x)).apply(lambda x: firstFound(x))
  # 住院医师 # 
    hco_list[i]['hco_Resident'] = hco_list[i].hospital_synopsis.apply(lambda x: Resident(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Resident'] = dept_list[i].dept_synopsis.apply(lambda x: Resident(x)).apply(lambda x: firstFound(x))
  # 主治医师 #  
    hco_list[i]['hco_Attending'] = hco_list[i].hospital_synopsis.apply(lambda x: Attending(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Attending'] = dept_list[i].dept_synopsis.apply(lambda x: Attending(x)).apply(lambda x: firstFound(x))
  # 护士 #
    hco_list[i]['hco_Nurse'] = hco_list[i].hospital_synopsis.apply(lambda x: Nurse(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Nurse'] = dept_list[i].dept_synopsis.apply(lambda x: Nurse(x)).apply(lambda x: firstFound(x))
  # 博士生导师 #
    hco_list[i]['hco_PhdAdvisor'] = hco_list[i].hospital_synopsis.apply(lambda x: PhDAdvisor(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_PhdAdvisor'] = dept_list[i].dept_synopsis.apply(lambda x: PhDAdvisor(x)).apply(lambda x: firstFound(x))
  # 硕士生导师 #
    hco_list[i]['hco_MasterAdvisor'] = hco_list[i].hospital_synopsis.apply(lambda x: MasterAdvisor(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_MasterAdvisor'] = dept_list[i].dept_synopsis.apply(lambda x: MasterAdvisor(x)).apply(lambda x: firstFound(x))    
  # 专家 #
    hco_list[i]['hco_Expert'] = hco_list[i].hospital_synopsis.apply(lambda x: Expert(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Expert'] = dept_list[i].dept_synopsis.apply(lambda x: Expert(x)).apply(lambda x: firstFound(x))
  # 教授 #
    hco_list[i]['hco_Professor'] = hco_list[i].hospital_synopsis.apply(lambda x: Professor(x)).apply(lambda x: firstFound(x))
    dept_list[i]['dept_Professor'] = dept_list[i].dept_synopsis.apply(lambda x: Professor(x)).apply(lambda x: firstFound(x))    


# 医生 #
for i in range(len(dcr_list)):
  # 性别 #
    dcr_list[i]['gender'] = dcr_list[i].doctor_synopsis.apply(lambda x: dcrGender(x)).apply(lambda x: firstFound(x))
  # 是否有博士学历 # {1: 有, 0: 无}
    dcr_list[i]['is_PhD'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '博士'))
  # 是否有硕士学历 #
    dcr_list[i]['is_master'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '硕士'))
  # 是否发表论文 #
    dcr_list[i]['has_publication'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '论文'))
  # 是否导师 #
    dcr_list[i]['is_mentor'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '导师'))
  # 是否参与临床试验 #
    dcr_list[i]['is_involved_in_clinical_trial'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '临床试验|新药|试验'))
  # 是否退休 #
    dcr_list[i]['is_retired'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '退休'))
  # 公开讲座 #
    dcr_list[i]['is_public_speaker'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '讲座'))
  # 会员 #
    dcr_list[i]['membership'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '学会会员|委员'))
  # 出国 #
    dcr_list[i]['study_abroad'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '留学'))
  # 专利 #
    dcr_list[i]['patent'] = dcr_list[i].doctor_synopsis.apply(lambda x: exist(x, '专利'))  
  # 本科院校 #
    dcr_list[i]['school'] = dcr_list[i].doctor_synopsis.apply(lambda x: grad(x)).apply(lambda x: firstFound(x))
  # 本科以上学历
    dcr_list[i]['grad_1'] = dcr_list[i].doctor_synopsis.apply(lambda x: grad(x)).apply(lambda x: secondFound(x))


# 合并医院、科室、医生数据 #
s1 = hco_list[0].columns
s2 = dept_list[0].columns
s_i = list(set(s1) & set(s2)) # hco_list & dept_list共有字段
s3 = dcr_list[0].columns
s_i_2 = list(set(s3) & (set(s1 | s2))) # hco_list & dept_list整合后和dcr_list的共有字段

interim = []
for i in range(len(raw_list)):
    t1 = dept_list[i].merge(hco_list[i], how = 'left', on = s_i) # 基于共有字段join
    t2 = dcr_list[i].merge(t1, how = 'left', on = s_i_2)
    interim.append(t2)
    print(len(t2))


# 将更新后的dataframe文件以xlsx格式导出
def save_xlsx(list_dfs, version):
    for i in range(len(list_dfs)):
        filename = list_dfs[i].province.unique()
        writer = pd.ExcelWriter(os.path.join(str(filename) + '.xlsx'))
        list_dfs[i].to_excel(writer, str(version))
        writer.save()

for i in range(len(raw_list)):
    print (i)
    print (raw_list[i].province.unique())

province_vol = []
province_nam = []
for i in range(len(interim)):
    t1 = len(interim[i])
    t2 = interim[i].province.unique()
    province_vol.append(t1)
    province_nam.append(t2)

data_profile = pd.DataFrame({'province': province_nam, 'volume': province_vol})
writer = pd.ExcelWriter(os.path.join(os.getcwd() + '/data_profile.xlsx'))
data_profile.to_excel(writer, 'Sheet1')
writer.save()

# dcr['doctor_synopsis_shortened'] = dcr.doctor_synopsis.apply(lambda x: numExtraction(x, alphanumeric_pat))

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





