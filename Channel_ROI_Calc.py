# Data source: Lantus # 

# baseline regression #

import pandas as pd 
import numpy as np 
from sklearn import linear_model 
from statsmodels.formula.api import ols
from pandas import ExcelWriter

promo = pd.read_excel("PromoMix.xlsx")

# Stocking algorithm #
	# Extract all input channels from raw data
channels = pd.Series(promo.columns)[4:].reset_index(drop = True)
	# Assign a initial retention rate to each channel (domain expertise required, can be improved later in modeling process)
channels_retention = pd.Series([0.9, 0.8, 0.7, 0.6, 0.7, 0.7, 0.7, 0.7, 0.8, 0.6, 0.7])
	# Calculate the initial mean (first month) by channel #
channels_mean_initial = []
for i in range(len(channels)):
	x = promo.loc[0:2,channels[i]].mean()
	channels_mean_initial.append(x)

channels_mean_initial = pd.Series(channels_mean_initial) # list - pandas object conversion

	# Construct channel-level data input
series = [channels, channels_retention, channels_mean_initial]
channels_input = pd.concat(series, axis = 1)
channels_input.columns = ['channel', 'retention_rate', 'channel_mean_initial']

	# Calculate the initial stk value for each channel
channels_m0 = promo[channels][0:1].transpose().reset_index()
channels_m0.columns = ['channel', 'first_month_mean']

	# Join channels_input and channels_m0
channels_input = pd.merge(channels_input, channels_m0)

	# Calculate stocking value for the first month
channels_input['channels_stk_m0'] = channels_input.first_month_mean*(1 - channels_input.retention_rate) + channels_input.channel_mean_initial*channels_input.retention_rate

	# Save channel_input file for further calculation use
writer = pd.ExcelWriter("channels_input.xlsx")
channels_input.to_excel(writer, 'stocking algorithm input')
writer.save()

	# For each channel, calculate the stocking value for each month under observation
		# Create an empty column to store stocking values
stk_names = []

for i in range(len(channels)):
	stk_names.append(channels[i] + '_stk')
	promo[stk_names[i]] = ""
	promo[stk_names[i]][0] = channels_input.iloc[i]['channels_stk_m0']

	# For each channel, obtain the stocking value for the full column
 for i in range(len(stk_names)):
 	for j in range(1, len(promo)):
 		y = promo[channels[i]][j] * (1 - channels_input.retention_rate[i]) + channels_input.retention_rate[i] * promo[stk_names[i]][j - 1]
 		promo[stk_names[i]][j] = y
# 		print(i, j, y)

	# Save and export the new file - stocked data will be saved for the regression model
writer = pd.ExcelWriter("raw_stocking.xlsx")
promo.to_excel(writer, 'raw and stocked')
writer.save()

	# Regress Sales_Volume against computed _stk variables
stk_cols = [col for col in promo.columns if 'stk' in col]
















