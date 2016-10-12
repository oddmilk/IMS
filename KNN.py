import requests

# direct link to the data set
data_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

# local path where the data set is to be saved
local_filename = "/Users/mengjichen/Desktop/iris.xlsx"

# download the file
r = requests.get(data_url)

# writes the data to a local file 
f = open(local_filename, 'w')


f = urllib.request.urlopen(link)
iris = f.read()
print (iris)
