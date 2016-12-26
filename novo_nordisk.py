"""

Time: Dec 20, 2016
@Author Oddmilk

"""


import pandas as pd
import numpy as np  
import os
import glob

# import xlsx files
infiles = glob.glob("*.xlsx")
raw = []

for f in infiles:
	data = pd.read_excel(f)
	data['filename'] = f
	raw.append(data)


#######################
# Data Pre-Processing #
#######################

# Recode dimensions: string to int
map_region = pd.read_excel('Code_Mapping.xlsx', 'region_mapping')
dic_region = dict(zip(map_region.raw, map_region.Code))

map_dept = pd.read_excel('Code_Mapping.xlsx', 'dept_mapping')
dic_dept = dict(zip(map_dept.raw, map_dept.Code))

map_type = pd.read_excel('Code_Mapping.xlsx', 'type_mapping')
dic_type = dict(zip(map_type.raw, map_type.Code))

map_product = pd.read_excel('Code_Mapping.xlsx', 'prod_mapping')
dic_product = dict(zip(map_product.raw, map_product.Code))

depts_mapping = pd.read_excel('Code_Mapping.xlsx', 'video_mapping')
dic_depts_video = dict(zip(depts_mapping.raw, depts_mapping.Code))




tag_input = raw[1]


# Split the column of string tag into a list of words
tags = tag_input['浏览页面标签']
list_tags = []

for i in range(len(tags)):
	if isinstance(tags[i], float):
		pass
	else:
		tags_sep = tags[i].split("，")
		list_tags.append(tags_sep)

# Convert list element into pandas series
for i in range(len(list_tags)):
	list_tags[i] = pd.Series(list_tags[i])

# Flatten the list
flatten = lambda l: [item for sublist in l for item in sublist]
tags_unique = pd.Series(flatten(list_tags)).unique()

# For each unique tag, count its occurrence
tag_data = []
tag_occurrence = []
for i in range(len(tags_unique)):
	x = tag_input.loc[tag_input['浏览页面标签'].str.contains(tags_unique[i], na = False)]
	tag_data.append(x)
	y = len(x)
	tag_occurrence.append(y)

tag_occurrence = pd.Series(tag_occurrence)
tags_1 = pd.DataFrame({'tag': tags_unique, 'occurrence':tag_occurrence}).reset_index()

from pandas import ExcelWriter
writer = pd.ExcelWriter("tag_count.xlsx")
tags_1.to_excel(writer, 'Sheet1')
writer.save()

# for each unique tag, count its occurrence by a given list of dimensions
occurrence_by_product = []
occurrence_by_region = []
occurrence_by_dept = []
occurrence_by_segment = []

for i in range(len(tag_data)):
	t1 = tag_data[i].groupby('子产品组').count().reset_index().ix[:,0:2]
	t2 = tag_data[i].groupby('大区').count().reset_index().ix[:,0:2]
	t3 = tag_data[i].groupby('客户科室').count().reset_index().ix[:,0:2]
	t4 = tag_data[i].groupby('MIX医生分级').count().reset_index().ix[:,0:2]
	occurrence_by_product.append(t1)
	occurrence_by_region.append(t2)
	occurrence_by_dept.append(t3)
	occurrence_by_segment.append(t4)

for i in range(len(occurrence_by_product)):
	occurrence_by_product[i] = occurrence_by_product[i].replace({"子产品组": dic_product})
	occurrence_by_segment[i] = occurrence_by_segment[i].replace({"MIX医生分级": dic_type})
	occurrence_by_dept[i] = occurrence_by_dept[i].replace({"客户科室": dic_dept})
	occurrence_by_region[i] = occurrence_by_region[i].replace({"大区": dic_region})

# for each tag, export occurrence and breakdown into one excel sheet
t_list = [occurrence_by_segment[1], occurrence_by_dept[1], occurrence_by_region[1], occurrence_by_product[1]]

def save_xlsx(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet_%s' % n)
    writer.save()
save_xls(list_dfs, xls_path)

for i in range(len(tags_unique)):
	u = [occurrence_by_product[i], occurrence_by_region[i], occurrence_by_dept[i], occurrence_by_segment[i]]
	p = os.path.join(str(i) + '.xlsx')
	save_xlsx(u, p)



#################
# Task 2: Video #
#################
import jieba

video_input = raw[2]
title_unique = video_input['视频标题'].unique()
title_joined = ", ".join(title_unique)
seg_list = list(jieba.cut(title_joined, cut_all = False)) # generator object - list conversion
titleset = list(set(seg_list)) # this returns non-duplicate elements in a list
meaningless_kw = [i for i, item in enumerate(titleset) if item is ' '] # find all the indexes where there is a ' '
del titleset[np.asarray(meaningless_kw)]

# recode department dimension
video_input = video_input.replace({"子产品组": dic_product})
video_input = video_input.replace({"MIX医生分级": dic_type})
video_input = video_input.replace({"大区": dic_region})
video_input = video_input.replace({"客户科室": dic_depts_video})


# for each keyword in the title, count the occurrence
title_kw_data = []
title_kw_occurrence = []

for i in range(len(titleset)):
	x = video_input.loc[video_input['视频标题'].str.contains(titleset[i], na = False)]
	title_kw_data.append(x)
	y = len(x)
	title_kw_occurrence.append(y)

# create title keyword table
title_kw_count = pd.DataFrame({'title_keyword': pd.Series(titleset), 'entries': pd.Series(title_kw_occurrence)}).reset_index()
# data output
writer = pd.ExcelWriter("/Users/mengjichen/Desktop/Advanced_Analytics/NN/Output/video_kw_count.xlsx")
title_kw_count.to_excel(writer, 'Sheet1')
writer.save()

##### Import the new tag as filtered by Janey #####
video_tag_v2 = pd.read_excel("video_tag_v2.xlsx")
v_tag = video_tag_v2.sort_values("entries", ascending = False)[0:12]
v_tag_index = v_tag.index


title_kw_by_product = []
title_kw_by_region = []
title_kw_by_dept = []
title_kw_by_segment = []

for i in range(len(title_kw_data)):
	t1 = title_kw_data[i].groupby('子产品组').count().reset_index().ix[:,0:2]
	t2 = title_kw_data[i].groupby('大区').count().reset_index().ix[:,0:2]
	t3 = title_kw_data[i].groupby('客户科室').count().reset_index().ix[:,0:2]
	t4 = title_kw_data[i].groupby('MIX医生分级').count().reset_index().ix[:,0:2]
	title_kw_by_product.append(t1)
	title_kw_by_region.append(t2)
	title_kw_by_dept.append(t3)
	title_kw_by_segment.append(t4)

for i in range(len(title_kw_by_segment)):
	title_kw_by_segment[i]['MIX医生分级'] = title_kw_by_segment[i]['MIX医生分级'].astype(int)
	title_kw_by_product[i]['子产品组'] = title_kw_by_product[i]['子产品组'].astype(int)


for i in range(len(titleset)):
	u = [title_kw_by_product[i], title_kw_by_region[i], title_kw_by_dept[i], title_kw_by_segment[i]]
	p = os.path.join('title_kw_' + str(i) + '.xlsx')
	save_xlsx(u, p)


#####################################
# Visualization 
#####################################

# A grid of pie charts
# palette to be used
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

palette = {1: '#2166ac',
	2: '#4393c3',
	3: '#92c5de',
	4: '#d1e5f0',
	5: '#ffffbf',
	6: '#fddbc7',
	7: '#f4a582',
	8: '#d6604d',
	9: '#b2182b'}

plt.rcParams['font.size'] = 6.0

# keyword-based data extraction & append
# Tangyi Pageview
pv_kw_index = tags_1.loc[tags_1.occurrence >= 10].index

d = []
the_grid = GridSpec(12,4)
tuples = [(x, y) for x in range(0,12) for y in range(0,4)]

for i in range(len(pv_kw_index)):
	d1 = occurrence_by_product[i] 
	d2 = occurrence_by_segment[i]
	d3 = occurrence_by_region[i]
	d4 = occurrence_by_dept[i]
	x = [d1, d2, d3, d4]
	d.append(x)

for i in range(len(d)):
	for j in range(len(d[i])):
#		print(j + 4*i)
		labels = np.asarray(d[i][j].iloc[:,0])
#		print(labels)
		fracs = np.asarray(d[i][j].iloc[:,1])
		plt.subplot(the_grid[tuples[j + 4*i]], aspect = 1)
		plt.pie(fracs, colors = [palette[k] for k in labels])


# video
v = []

tuples = [(x, y) for x in range(0,1) for y in range(0,4)]

for i in range(len(v_tag_index)):
	v1 = title_kw_by_product[i]
	v2 = title_kw_by_segment[i] 
	v3 = title_kw_by_region[i] 
	v4 = title_kw_by_dept[i] 
	x = [v1, v2, v3, v4]
	v.append(x)


labels = []
fracs = []

for i in range(len(v)):
	for j in range(len(v[i])):
		l = np.asarray(v[i][j].iloc[:,0])
		labels.append(l)
		f = np.asarray(v[i][j].iloc[:,1])
		fracs.append(f)


the_grid = GridSpec(12,4)



for i in range(12):
	for j in range(4):
		plt.subplot(the_grid[tuples[i][j]], aspect = 1)
		plt.pie(fracs[j + 4*i], labels = labels[t + 4*i], colors = [palette[k] for k in labels[t + 4*i]], autopct = '%1.1f%%', shadow=True)

savefig(os.path.join(str(11) + '.pdf'))
plt.clf()





############ Task 1 ##################
the_grid = GridSpec(12,4)
tuples = [(x, y) for x in range(0,12) for y in range(0,4)]

d = []
labels = []
fracs = []

for i in range(len(pv_kw_index)):
	d1 = occurrence_by_product[i]
	d2 = occurrence_by_segment[i]
	d3 = occurrence_by_region[i]
	d4 = occurrence_by_dept[i]
	d.append([d1, d2, d3, d4])

	lab = []
	fr = []

	for j in range(4):
		l = np.asarray(d[i][j].iloc[:,0])  # for each of the chosen tag, return the frac labels 
		lab.append(l)
		labels.append(lab)
		f = np.asarray(d[i][j].iloc[:,1]) # frac value
		fr.append(f)
		fracs.append(fr)

	for j in range(4):
		plt.subplot(the_grid[tuples[j + 4*i]], aspect = 1)
		plt.pie(fracs[j], labels = labels[j], colors = [palette[k] for k in labels[j]], autopct = '%1.1f%%', shadow=True)


	p_name = os.path.join(str(i) + '.pdf')
	plt.savefig(p_name)
	plt.close()

plt.savefig('PV_tags.pdf')



#####################
# Segment-driven
#####################
import seaborn as sns

p = []
for i in range(len(pv_kw_index)):
	x = occurrence_by_segment[i]
	p.append(x)

p = pd.concat(p, keys = tags_unique[pv_kw_index]).reset_index() 

ax = sns.barplot(x = "MIX医生分级", y = "用户id", hue = "level_0", data = p, palette = "RdBu")
plt.savefig('tags_by_segment.pdf')


video_bar = []
for i in range(len(v_tag_index)):
	x = title_kw_by_product[i]
	video_bar.append(x)

v_bar = pd.concat(video_bar, keys = v_tag_index).reset_index()
ax = sns.barplot(x = "子产品组", y = "用户id", hue = "level_0", data = v_bar, palette = "RdBu")
plt.savefig('video_product.pdf')
plt.clf()


#################################
### Analysis of visiting time ###
#################################
# Data subsetting 
	# Split video watching time
dt = pd.DatetimeIndex(video_input['学习时间'])
video_input['hour'] = dt.hour.astype(int)
video_input['month'] = dt.month.astype(int)
Feb = video_input[dt.month == 2]
Feb_id = Feb['用户id'].unique()

# Group video view data by hour
Feb_grp = Feb.groupby('hour')
Feb_hourly_view = Feb_grp['用户id'].count().reset_index()

sns.set_style("whitegrid")
ax = sns.stripplot(x = Feb_hourly_view.hour, y = Feb_hourly_view['用户id'], color = "#203d75", size = 7)
fig = ax.get_figure()
fig.savefig('video_view_by_hour.pdf')


# Group video view data by hour and region
hospital_region = pd.read_excel('/Users/mengjichen/Desktop/Advanced_Analytics/NN/Input/hospital_region.xlsx')
hr = hospital_region[['area','hospitalname','hospitallevel']].drop_duplicates()


#################################
### Dropout rate ###
#################################
# Data loading
pool = pd.read_excel('/Users/mengjichen/Desktop/Advanced_Analytics/NN/Input/Pool.xlsx', '8k')
pool_dt = pd.DatetimeIndex(pool['学习时间'])
pool['month'] = pool_dt.month.astype(int)

pool_grp = pool.groupby('month')
pool_monthly = pool_grp['tangyi_user_id'].nunique().reset_index()

ax = sns.stripplot(x = pool_monthly.month, y = pool_monthly['tangyi_user_id'], color = "#203d75", size = 7)
fig = ax.get_figure()
fig.savefig('pool_retention.pdf')

pool_feb = pool[pool.tangyi_user_id.isin(Feb_id)]
pool_feb_grp = pool_feb.groupby('month')
pool_feb_monthly = pool_feb_grp['tangyi_user_id'].nunique().reset_index()
pool_feb_monthly.columns = ['month', 'feb_user']
pool_monthly.columns = ['month', 'all_user']
pool_retention = pool_monthly.merge(pool_feb_monthly, how = 'left', on = 'month').fillna(0).astype(int)

f, ax = plt.subplots()
sns.barplot(x = "month", y = "all_user", data = pool_retention, color = "#203d75")
sns.barplot(x = "month", y = "feb_user", data = pool_retention, color = "#6ec8ea")
fig = ax.get_figure()
fig.savefig('pool_feb_retention.pdf')
