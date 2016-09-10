import requests
from bs4 import BeautifulSoup
import html.parser
import time   # to get time of python program execution
from random import randint
import sys
from IPython.display import clear_output
import pandas as pd
import urllib.parse as urlparse
from urllib.parse import urlencode


url_endpoint = 'https://www.duckduckgo.com'
mydict = {'q': 'whee! Stanford!!!', 'something': 'else'}
resp = requests.get(url_endpoint, params=mydict)

# url end point
url_endpoint = 'http://www.guahao.com/search/expert?'

# query string 1: specialty
param_wkp = ['内科', '外科', '妇产科', '皮肤性病科', '骨科', '耳鼻咽喉科']

# query string 2: location
# construct a list of urls filtering by province #
prov = {'北京': 1, '上海': 2, '天津': 3, '重庆': 4, '辽宁': 5, '吉林': 6, '黑龙江': 7, '山西': 8, '陕西': 9, '宁夏': 10, '甘肃': 11, '青海': 12, '新疆': 13,
'西藏': 14, '四川': 15, '河北': 16, '云南': 17, '贵州': 18, '湖北': 19, '河南': 20, '山东': 21, '江苏': 22, '安徽': 23, '浙江': 24, '江西': 25, '福建': 27,
'广东': 29, '湖南': 30, '广西': 31, '海南': 32, '内蒙古': 33}

# Given specialty (e.g. 内科), for each province, extract the total number of pages 
master_url = "http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=内科&pi=22&p=江苏&ci=all&c=不限&pageNo=1" 
params = [{'pi': 1,'p':'北京'},
{'pi': 2, 'p': '上海'},
{'pi': 3, 'p': '天津'},
{'pi': 4, 'p': '重庆'},
{'pi': 5, 'p': '辽宁'},
{'pi': 6, 'p': '吉林'},
{'pi': 7, 'p': '黑龙江'},
{'pi': 8, 'p': '山西'},
{'pi': 9, 'p': '陕西'},
{'pi': 10, 'p': '宁夏'},
{'pi': 11, 'p': '甘肃'},
{'pi': 12, 'p': '青海'},
{'pi': 13, 'p': '新疆'},
{'pi': 14, 'p': '西藏'},
{'pi': 15, 'p': '四川'},
{'pi': 16, 'p': '河北'},
{'pi': 17, 'p': '云南'},
{'pi': 18, 'p': '贵州'},
{'pi': 19, 'p': '湖北'},
{'pi': 20, 'p': '河南'},
{'pi': 21, 'p': '山东'},
{'pi': 22, 'p': '江苏'},
{'pi': 23, 'p': '安徽'},
{'pi': 24, 'p': '浙江'},
{'pi': 25, 'p': '江西'},
{'pi': 27, 'p': '福建'},
{'pi': 29, 'p': '广东'},
{'pi': 30, 'p': '湖南'},
{'pi': 31, 'p': '广西'},
{'pi': 32, 'p': '海南'},
{'pi': 33, 'p': '内蒙古'}] # input param (dict prov)

# destination: {'pi', 'p', 'pageNo'}


url_parts = list(urlparse.urlparse(master_url))
query = dict(`)  # query component is indexed at 4
list_url = []  # for a given specialty, this list stores first returned page result for every province

# loop through the list of dictionaries
for i in range(len(params)):
    query.update(params[i]) # params is the dict parameter to update query
    url_parts[4] = urlencode(query)
    paramed_url = (urlparse.urlunparse(url_parts))
    list_url.append(paramed_url)


# for a given specialty, extract the total number of returned pages for each province 
url_range = [] 

for url in list_url:
    res = requests.get(url)
    soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
    div = soup.findAll("div", {"class": "other-info"})
    for a in div:
        label = a.find('label')
        label_range = label.get_text() # this returns the total page results under each provinc
        url_range.append(label_range)

# convert all strings in the list to integers
url_range = list(map(int, url_range))

sum(int(i) for i in url_range) # total amount of result pages of 内科 in all provinces

for x in url_range:
    for i in range(url_range[x]):
        params


for i in range(len(params)):
    params[i]['pageNo'] = url_range[i]
    query.update(params[i]) # params is the dict parameter to update query
    url_parts[4] = urlencode(query)
    paramed_url = (urlparse.urlunparse(url_parts))
    list_url.append(paramed_url) # this returns a list of last returned page result for each province


# for each workplace in each province: 31*6, construct an url link:
    # 江苏
JS_internal_medicine = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=内科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(790)]
JS_general_surgery = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=外科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(498)]
JS_obgyn = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=妇产科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(256)]
JS_dermatology = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=皮肤性病科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(57)]
JS_orthopedics = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=骨科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(181)]
JS_ENT = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=耳鼻咽喉科&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(74)]

JS = JS_general_surgery
JS = JS_obgyn
JS = JS_dermatology
JS = JS_orthopedics
JS = JS_ENT

    # JX    


link_table = [] # create an empty list to store extracted HTML data

list_hcp_url = []
list_hcp_name = []
list_hcp_subtype = [] # professional subtype: 主任，副主任，主治，副主治医师，etc
list_wkp = []
list_hco = []

for link in JS:
    res = requests.get(link)  # create a response object
    soup = BeautifulSoup(res.text.encode("utf-8"), "lxml") # The soup object contains all of the HTML in the original document
    table = soup.findAll("div", {"class": "g-doc-baseinfo"})  # this div is where individual profile, title, wkp, hospital all live
    link_table.append(table)
    hcp_url = []
    hcp_name = []
    hcp_subtype = []
    wkp = []
    hco = []
    # for each extracted individual, extract the five things we want: Name, title, wkp, hospital, profile source
    for div in table:
        a = div.findAll('a')[1]
        b = div.findAll('a')[2]
        c = div.findAll('a')[3]
        hcp_url.append(a['href']) # extract profile src (url)
        hcp_name.append(div.dt.contents[1].get_text().strip())
        hcp_subtype.append(div.dt.contents[2].strip())  # professional subtype is stored as navigatestring
        wkp.append(b.get_text().strip())
        hco.append(c.get_text().strip())
    list_hcp_url.append(hcp_url)
    list_hcp_name.append(hcp_name)
    list_hcp_subtype.append(hcp_subtype)
    list_wkp.append(wkp)
    list_hco.append(hco)

for idx in enumerate(JS):
    print (idx)

# merge/flatten list of lists; convert into a data frame; write to excel
def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list

out_hcp_url = flatten(list_hcp_url)
out_hcp_name = flatten(list_hcp_name)
out_hcp_subtype = flatten(list_hcp_subtype)
out_wkp = flatten(list_wkp)
out_hco = flatten(list_hco)

# create a dict from flattened lists of data and then load that into the data frame
hcp_data_internal_medicine = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

hcp_data_general_surgery = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

hcp_data_oygcn = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

hcp_data_dermatology = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

hcp_data_orthopedics = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

hcp_data_ENT = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])

list_hcp = [hcp_data_internal_medicine, hcp_data_general_surgery, hcp_data_oygcn, hcp_data_dermatology, hcp_data_orthopedics, hcp_data_ENT]

from pandas import ExcelWriter
def save_xls(list_dfs, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()

JS_HCP = save_xls(list_hcp, '/Users/mengjichen/Desktop/WebScraping/')










