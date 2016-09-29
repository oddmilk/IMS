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
    for i in range(len(param)):
        query.update(param[i]) 
        url_parts[4] = urlencode(query)
        paramed_url = (urlparse.urlunparse(url_parts))
        url_list.append(paramed_url)
    return(url_list)

# given all query parameters, return a list containing number of page results
def getPageNo(list_urls):
    url_range = [] 
    for url in list_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
        url_range.append(hcp_range)
        div = soup.findAll("div", {"class": "other-info"})
        for a in div:
            label = a.find('label')
            label_range = label.get_text() # this returns the total page results under each province
            label_range = int(label_range)
            url_range.append(label_range)
# convert all strings in the list to integers
    url_range = list(map(int, url_range))
    return(url_range)



def getHcpNo(list_urls):
    hcp_range = []
    for url in list_urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text.encode("utf-8"), "lxml")
        strong = soup.findAll('strong')
        strong = str(strong)
        try:
            n_hcp = [int(s) for s in strong.split() if s.isdigit()][0]
        except IndexError:
            n_hcp = 'null'
#        print(n_hcp)
        hcp_range.append(n_hcp)
    return(hcp_range)


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

