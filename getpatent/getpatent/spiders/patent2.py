# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from getpatent.items import GetpatentItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random
from getpatent.settings import FIELD 
from getpatent.spiders.parse_info import get_info,write_relpatents
infilename = 'relpatents.txt'
outfilename = 'relpatents2.txt'

Url = 'https://www.google.com'
class Patent2Spider(scrapy.Spider):
    name = 'patent2'
    
    allowed_domains = ['www.google.ca','www.google.com']
    
    # start_urls = []
    scrawl_url = set()
    peopleUrl =set()#记录以爬
    with open(infilename,'r') as f:
    	lists= f.readlines()
    for url in lists:
    	scrawl_url.add(url[0:-1])
    start_urls = list(scrawl_url)

    def parse(self,response):
        item = GetpatentItem()
        item['Url'] = response.url

        sel = Selector(response)
        information = get_info(sel)

        item['Title'] = information['Title']
        item['Abstract'] =information['Abstract']
        item['Publication_number'] = information['Publication_number']
        item['Publication_type'] = information['Publication_type']
        item['Publication_date'] =information['Publication_date']
        item['Original_Assignee'] = information['Original_Assignee']
        item['Filing_date'] = information['Filing_date']
        item['Application_number'] = information['Application_number']
        item['Priority_date'] = information['Priority_date']
        item["Inventors"] = information["Inventors"]
        item['Applicant'] = information['Applicant']
        item["Export_Citation"] = information["Export_Citation"]
        item["Also_published_as"] = information["Also_published_as"]
        item['External_Links'] = information['External_Links']
        item['Cited_patent'] = information['Cited_patent']
        item['Referenced_by'] = information['Referenced_by']
        item['Classification'] = information['Classification']
        
        write_relpatents(outfilename,information['rel_patents'])
        yield item