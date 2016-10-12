# Chapter 6
import pandas as pd 

# read exel file
data = pd.read_excel("/Users/mengjichen/Desktop/EU_itinerary.xlsx", sheetname = 'Accommodation')

# read data from url (web scraping)
from lxml.html import parse
from urllib import urlopen
parsed = parse(urlopen('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'))
doc = parsed.getroot()
