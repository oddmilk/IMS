# -*- coding: utf-8 -*-
import sys
import scrapy
from datetime import datetime
from scrapy.http import Request, FormRequest, TextResponse
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.selector import Selector
import logging
from ..items import HosItem
#from scrapy.stats import Stats


# 全国所有内科医生
html = 'https://www.guahao.com/search/expert?q=内科'

class Crawler(CrawlSpider):
    name = "crawler"
    allowed_domains = ["guahao.com"]
    start_urls = [
        "https://www.guahao.com/search?q=内科"
    ]

    rules = [
        Rule(LinkExtractor(allow = ('\?Dept=\w+.*')),
        callback = 'parse_table', follow = True),x

        Rule(LinkExtractor(allow = ('\?Dept=\w+.*week=2')),
        callback = 'parse_table', follow = True)
     ]


# 2016-09-05
import requests
from bs4 import BeautifulSoup
import html.parser
import time   # to get time of python program execution
from random import randint
import sys
from IPython.display import clear_output


# 2016-09-06

# need to construct a list of urls filtering by province #
param_prov = ['湖南', '湖北', '广东', '广西', '河南', '河北', '山东', '山西', '江苏', 
'浙江', '江西', '黑龙江', '新疆', '云南', '贵州', '福建', '吉林', '安徽', '四川', '海南',
'西藏', '宁夏', '辽宁', '青海', '甘肃', '陕西', '内蒙古', '北京', '上海', '天津', '重庆']

# construct a list of urls filtering by workplace # 
param_wkp = ['内科', '外科', '妇产科', '皮肤性病科', '骨科', '耳鼻咽喉科']

# extract page range for each combination
param_page_range = [790, 498, 255, 57, 181, 74]

# for each workplace in each province: 31*6, construct an url link:
    # 江苏， 内科
    # range extraction
JS_internal_medicine = ['http://www.guahao.com/search/expert?iSq=&fhc=&fg=&q=' + param_wkp[0] + '&pi=22&p=江苏&ci=all&c=不限&pageNo=' + str(i+1) for i in range(param_page_range[0])]

link_table = [] # create an empty list to store extracted HTML data
list_hcp_url = []
list_hcp_name = []
list_wkp = []
list_hco = []
list_hcp_subtype = [] # professional subtype: 主任，副主任，主治，副主治医师，etc

for link in JS_internal_medicine:
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

for idx in enumerate(JS_internal_medicine):
    print (idx)

# merge/flatten list of lists; convert into a data frame; write to excel
import itertools
chain_hco = itertools.chain(*list_hco)
list_hco = list(chain_hco)
























