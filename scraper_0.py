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
        callback = 'parse_table', follow = True),

        Rule(LinkExtractor(allow = ('\?Dept=\w+.*week=2')),
        callback = 'parse_table', follow = True)
     ]


# 2016-09-04
import requests
from bs4 import BeautifulSoup
import HTMLParser
import time
from random import randint
import sys
from IPython.display import clear_output

links = ['http://www.ipeen.com.tw/search/all/000/1-100-0-0/?p=' + str(i+1) + 'adkw=東區&so=commno' for i in range(10)]
links = ['http://www.guahao.com/search/expert?q=内科&pageNo=' + str(i+1) for i in range(8470)]

physician_links=[]

for link in links:
    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode("utf-8"))
    physician_table = soup.findAll('dt')
    ##關在a tag裡的網址抓出來
    for physician_link in physician_table:
        link = 'http://www.ipeen.com.tw' + [tag['href'] for tag in shop_link.findAll('a',{'href':True})][0]
        shop_links.append(link)
    ##避免被擋掉，小睡一會兒
    time.sleep(1)