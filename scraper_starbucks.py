import requests
from bs4 import BeautifulSoup
import html.parser
import time   # to get time of python program execution
from random import randint
import sys
from IPython.display import clear_output
import pandas as pd
import numpy as np
import urllib.parse as urlparse
from urllib.parse import urlencode
import math

# Loc: Shanghai (code: 1)
# Target: Starbucks
# base url: www.dianping.com

# for each returned retail store, extract shop url 

links = ['http://www.yelp.com/search?find_desc=Starbucks&find_loc=Boston,+MA,+United+States&' + 'start=' + str(i*10+30) for i in range(5)]

shop_links=[]
for link in links:
    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
    shop_table = soup.findAll('h3',{'class':'search-result-title'})
    ##關在a tag裡的網址抓出來
    for shop_link in shop_table:
        link = 'http://www.yelp.com' + [tag['href'] for tag in shop_link.findAll('a',{'href':True})][0]
        shop_links.append(link)
    ##避免被擋掉，小睡一會兒
    time.sleep(1)


link = links[0]
res = requests.get(link)
soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
shop_table = soup.findAll('h3',{'class':'search-result-title'})
##關在a tag裡的網址抓出來
for shop_link in shop_table:
    link = 'http://www.yelp.com' + [tag['href'] for tag in shop_link.findAll('a',{'href':True})][0]
    shop_links.append(link)



# for each shop, extract review data that contains the keyword '拿铁'


