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


#### Functions ####
# loop through dict query string params to construct all page urls to be looped through
def getURL(param, query, url_parts, url_list):
    for i in range(len(param)):  # list indices can only be string (int is not accepted)
        query.update(param[i])  # update function will update values in key-value pairs in dictionary param
        url_parts[4] = urlencode(query) # extract the part of query string, which is indexed at 4
        paramed_url = (urlparse.urlunparse(url_parts))
        url_list.append(paramed_url)
    return(url_list)

# for each input url (with parameters in query strings set to certain values), return a list containing number of page results
def getPageNo(list_urls):
    url_range = [] # define an empty list to store page results 
    for url in list_urls:
        res = requests.get(url) # for each url, get all contents from the html page
        soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
        div = soup.findAll("div", {"class": "other-info"})
        for a in div:
            label = a.find('label') # numeber of total page results returned was stored between <label> and </label>
            label_range = label.get_text() # extract the text betwee label tags 
#            label_range = int(label_range) 
            url_range.append(label_range)
    url_range = list(map(int, url_range)) # convert all strings in the list to integers
    return(url_range)

# for each given url, extract the number of total patients found (this function is more robust than getPageNo as for certain provinces there is simply 1 returned page result)
def getHcpNo(list_urls):
    hcp_range = []
    for url in list_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
        strong = soup.findAll('strong') # in guahao.com's case, number of physicians found is stored between <strong> tags
        strong = str(strong) # data type conversion: bs4.element.resultSet to string
        try:
            n_hcp = [int(s) for s in strong.split() if s.isdigit()][0]
        except IndexError:
            n_hcp = 'null' # oddly enough there are cases where there's no physician found
#        print(n_hcp)
        hcp_range.append(n_hcp)
    return(hcp_range)

# flatten list of lists
def flatten(input_list):
    output_list = []
    for element in input_list:
        if type(element) == list:
            output_list.extend(flatten(element))
        else:
            output_list.append(element)
    return output_list


# Construct the dict of query string params: {'pi', 'p', 'pageNo'}
    # param 1: workplace
param_q =  ['内科', '外科', '妇产科', '皮肤性病科', '骨科', '耳鼻咽喉科']
    # param 2: location
        # generate a list of consecutive numbers
        # remove element 28 from the list as it is not encoded with any location information
param_loc = list(range(34)) # [1,2,3...,33]
del param_loc[0]
#del param_loc[13] # remove Tibet
del param_loc[25] # no province is assigned
del param_loc[26] # no province is assigned
    # Expand param 1 & 2 to equal length to allow for the creation of a list of dictionaries using paired values from both expanded params
param_q_expanded = list(np.repeat(param_q, 31))
param_loc_expanded = param_loc*6
    # Assign values from param_q_expanded & param_loc_expanded to an initialized dictionary
list_dic = []
for x in range(len(param_q_expanded)):
    q_loc_level = {'q': param_q_expanded[x], 'pi': param_loc_expanded[x]}
    list_dic.append(q_loc_level)

    # param 3: pageNo
        # this param cannot be pre-defined as it is a function of param_q & param_loc
        # range value can only be extracted by visiting the first returned page
base_url = "http://www.guahao.com/search/expert?q=内科&pi=1&ci=all&c=不限&pageNo=1" # param pi & p are bundled
url_parts = list(urlparse.urlparse(base_url))
query = dict(urlparse.parse_qsl(url_parts[4]))  # query component is indexed at 4

get_range = []
URL2GetPageNo = getURL(list_dic, query, url_parts, get_range)
HCPFound = getHcpNo(URL2GetPageNo) # each number (after math operation) should be converted to number of pages to be looped through

    # find all null HCPFound
def find(HCPFound, x):
    return [i for i, x in enumerate(HCPFound) if x == 'null'] # this returns: 10, 106, 110

HCPFound[10] = 1481 # somehow this number was not extracted
HCPFound[110] = 47
HCPFound[106] = 0
del HCPFound[106]
del list_dic[106]

HCP_Pages = []
for x in HCPFound:
    Page_X = math.ceil(x/12)
    HCP_Pages.append(Page_X)

    # for each value in HCP_Pages, construct a list of consecutive numbers
list_pages = []
for i in range(len(HCP_Pages)):
    list4loop = list(range(HCP_Pages[i]+1))
    del list4loop[0]
    list_pages.append(list4loop)

# Internal Medicine
list_internal_medicine = list_pages[0:32]
dic_internal_medicine = list_dic[0:31]
rep_internal_medicine = HCP_Pages[0:31]

# General surgery
dic_GS = list_dic[31:62]
rep_GS = HCP_Pages[31:62]
list_GS = list_pages[31:62]

# Gynecology
dic_GY = list_dic[62:93]
rep_GY = HCP_Pages[62:93]
list_GY = list_pages[62:93]

# Dermatology
dic_DERM = list_dic[93:123]
rep_DERM = HCP_Pages[93:123]
list_DERM = list_pages[93:123]

# Orthopedics
dict_ORTH = list_dic[123:154]
rep_ORTH = HCP_Pages[123:154]
list_ORTH = list_pages[123:154]

# ENT
dict_ENT = list_dic[154:185]
rep_ENT = HCP_Pages[154:185]
list_ENT = list_pages[154:185]

print(rep_ENT)
for x in list_ENT:
    print (len(x))

    ### using list_pages[0] at a length of 716 as an exmaple ###
q_im = list(np.repeat(param_q[3], sum(list_DERM)))
loc_im = []

param_loc_2 = param_loc[:]
del param_loc_2[13]

for i in range(len(rep_DERM)):
    x = list(np.repeat(param_loc_2[i], rep_DERM[i]))
    loc_im.append(x)

loc_im = flatten(loc_im)
list_DERM = flatten(list_DERM) 

list_params_im = []
for i in range(len(list_DERM)):
    params_im = {'q': q_im[i], 'pi': loc_im[i], 'pageNo': list_DERM[i]}
    list_params_im.append(params_im)
    
list_url2loop = []  # create an empty list to store URLs to be looped through
url2Loop = getURL(list_params_im, query, url_parts, list_url2loop)

link_table = [] # create an empty list to store extracted HTML data
list_hcp_url = []
list_hcp_name = []
list_hcp_subtype = [] # professional subtype: 主任，副主任，主治，副主治医师，etc
list_wkp = []
list_hco = []

for link in url2Loop:
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
        try:
            a = div.findAll('a')[1]
            b = div.findAll('a')[2]
            c = div.findAll('a')[3]
        except IndexError:
            a = 'null'
            b = 'null'
            c = 'null'
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

for idx in enumerate(url2Loop):
    print (idx)

out_hcp_url = flatten(list_hcp_url)
out_hcp_name = flatten(list_hcp_name)
out_hcp_subtype = flatten(list_hcp_subtype)
out_wkp = flatten(list_wkp)
out_hco = flatten(list_hco)

# create a dict from flattened lists of data and then load that into the data frame
hcp_data_DERM = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])
# save to txt
hcp_data_DERM.to_csv(r'/Users/mengjichen/Desktop/WebScraping/hcp_data_DERM.txt', header=None, index=None, sep=' ', mode='a')


hcp_data_ORTH = pd.DataFrame({'name': out_hcp_name, 'subtype': out_hcp_subtype, 'workplace': out_wkp, 'hospital': out_hco, 'url': out_hcp_url},
    columns = ['name', 'subtype', 'workplace', 'hospital', 'url'])
# save to txt
hcp_data_ORTH.to_csv(r'/Users/mengjichen/Desktop/WebScraping/hcp_data_ORTH.txt', header=None, index=None, sep=' ', mode='a')

# Print the ANSI escape sequence to clear the screen 
sys.stderr.write("\x1b[2J\x1b[H") 

