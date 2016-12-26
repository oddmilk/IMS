# Apply value_counts to multiple categorical variables in the data
	# Param: data frame, variables that contain unique values to be counted 
	# Output: a data frame of objects containing counts for each variable
def Value_Counts(df, vars):
	value_counts = df[vars].apply(pd.Series.value_counts)  
	return value_counts

# Compute count and percentage for each value in a categorical variable
	# Param: data frame, categorical variable
	# Output: a data frame indexed by variable labels, counts, percentages
def Value_CP(df, var):
	cnt = var.value_counts(dropna = True)
	cnt = pd.DataFrame(cnt).reset_index()
	cnt.columns = ['labels', 'count']
	cnt['percent'] = cnt['count']/cnt['count'].sum()
	cnt['percent'] = cnt['percent'].round(decimals = 3)
	return cnt





