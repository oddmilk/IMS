df = pd.DataFrame({'key1': ['a','a','b','b','a'],
				'key2': ['one','two','one','two','one'],
				'data1': np.random.randn(5),
				'data2': np.random.randn(5)})

df

grouped = df['data1'].groupby(df['key1'])

# iterating over groups #
for name, group in df.groupby('key1'):
	print(name)
	print(group)

for (k1, k2), group in df.groupby(['key1', 'key2']):
	print (k1, k2)
	print (group)

# compute a dict of the data pieces as a one-liner
pieces = dict(list(df.groupby('key1')))

