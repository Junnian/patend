# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from getpatent.items import GetpatentItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random
from getpatent.settings import FIELD,key1s,key2s
from getpatent.spiders.parse_info import get_info,write_relpatents

'''
aerospace第五页
https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
Biomedical engineering空格不用加下滑线

'''

Url = 'https://www.google.com'
import os,sys

print "__file__=%s" % __file__
outfilename = 'relpatents.txt' 
class ScholarSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['www.google.ca','www.google.com']
    start_urls = []
    for key in key1s:
        file_ = 'new/'+key+'.txt'
        with open(file_,'r') as f:
            list_ = f.readlines()
            for i in list_:
                start_urls.append(i)
                if ' ' in i:
                    i=i.replace(' ','_')
                    start_urls.append(i)#也就是说有下划线，没下划线的都要
    
    for key in key2s:
        file_ = 'key/'+key+'.txt'
        with open(file_,'r') as f:
            list_ = f.readlines()
            for i in list_:
                start_urls.append(i)
                if ' ' in i:
                    i=i.replace(' ','_') 
                    start_urls.append(i)#也就是说有下划线，没下划线的都要


    scrawl_ID = set(start_urls)  # 记录待爬
    finish_ID = set()  # 记录已爬
    peopleUrl = set() #记录已经爬的主页

    #下一个领域的开始放在前一个领域之后
    def start_requests(self):
        #只进行一次
        if self.scrawl_ID.__len__():
            print self.scrawl_ID.__len__()
            field = self.scrawl_ID.pop()
            self.finish_ID.add(field)  # 加入已爬队列
            # field = 'aerospace'
                   # https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
            url = 'https://www.google.com/search?q='+field+'&tbm=pts&start=00'+'&sa=N'
            # yield Request(url=url, callback=self.parse1)
            req = Request(url= url,callback = self.parse1)
            yield req
        
    def parse1 (self, response):
        #这个解析函数先处理每个领域第一页的人，用selector

        #得到专利详情页
        sel = Selector(response)
        detailurls = sel.xpath('//*[@class="r"]//a[contains(@href,"/patents/")]/@href').extract()
        reqs = []
        for url in detailurls:
            yield Request(url = url,callback = self.parse_info,dont_filter=True)
            # yield Request(url = url,callback = parse_info,dont_filter=True)

        nexturl = sel.xpath('//*[text()="Next"]/parent::*/@href').extract()
        nexturl2 = sel.xpath('//*[text()="Next"]/@href').extract()
        nexturl_1= response.xpath('//*[@class="b"]/a/@href').extract()
        nexturl_2 = response.xpath('//*[@class="b navend"]/a/@href').extract()
        print('---------------nexturl--------------nexturl',nexturl)
        print('---------------nexturl2--------------nnexturl2',nexturl2)
        print('-----------nexturl_1----------------nexturl_1',nexturl_1)
        print('-----------nexturl_2----------------nexturl_2',nexturl_2)

        #开是构造下一页链接
        url = 0
        if len(nexturl)==1:
            url = Url+nexturl[0]
                # yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        elif len(nexturl2)==1:
            print('-------------222---------------nexturl2',nexturl2)
            if nexturl2:
                url = Url+nexturl2[0]
                # yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        elif len(nexturl_2)==1: 
            print('-----------5555----------------nexturl_2',nexturl_2)
            url = Url+nexturl_2[0]

        if url==0: #就是前边的几个判断都没有提取到url，就只能强行拼一个
            print('-----------8----------------')
            nowurl = response.url
            #得到下一页页码
            a = nowurl.split('start=')
            b = a[-1].split('&')
            c = b[0]
            N = int(c)
            N = N+10

            #得到当前关键词
            a = nowurl.split('q=')
            b = a[1].split('&')
            key = b[0]
         
            url = 'https://www.google.com.hk/search?q='+key+'&tbm=pts&start='+str(N)+'&sa=N'
            filename = response.url+'.txt'
            with open('filename','a+') as f:
                f.write('1111')
                f.write(response.body)
        yield Request(url = url,callback = self.parse2,dont_filter=True)
        
            
    def parse2(self,response):
        #得到专利详情页
        sel = Selector(response)
        detailurls = sel.xpath('//*[@class="r"]//a[contains(@href,"/patents/")]/@href').extract()
        reqs = []
        for url in detailurls:
            yield Request(url = url,callback = self.parse_info,dont_filter=True)
            # yield Request(url = url,callback = parse_info,dont_filter=True)


        nexturl = sel.xpath('//*[text()="Next"]/parent::*/@href').extract()
        nexturl2 = sel.xpath('//*[text()="Next"]/@href').extract()
        nexturl_1= response.xpath('//*[@class="b"]/a/@href').extract()
        nexturl_2 = response.xpath('//*[@class="b navend"]/a/@href').extract()
        print('---------------nexturl--------------nexturl',nexturl)
        print('---------------nexturl2--------------nnexturl2',nexturl2)
        print('-----------nexturl_1----------------nexturl_1',nexturl_1)
        print('-----------nexturl_2----------------nexturl_2',nexturl_2)


        #开是构造下一页链接
        url = 0
        if len(nexturl)==1:
            url = Url+nexturl[0]
            yield Request(url = url,callback = self.parse2,dont_filter=True)
        elif len(nexturl_1)==2:
            print('-----------3----------------nexturl_1',nexturl_1)
            url = Url+nexturl_1[1]
            yield Request(url = url,callback = self.parse2,dont_filter=True)
        elif len(nexturl_2)==2: 
            print('-----------4444----------------nexturl_2',nexturl_2)
            url = nexturl_2[1]
            yield Request(url = Url+url,callback = self.parse2,dont_filter=True)

        elif len(nexturl_2)==0 and len(nexturl_1)==0 : #就是前边的几个判断都没有提取到url，就只能强行拼一个
            print('--q---------8----------------')
            nowurl = response.url
            #得到下一页页码
            a = nowurl.split('start=')
            b = a[-1].split('&')
            c = b[0]
            N = int(c)
            N = N+10

            #得到当前关键词
            a = nowurl.split('q=')
            b = a[1].split('&')
            key = b[0]
         
            url = 'https://www.google.com.hk/search?q='+key+'&tbm=pts&start='+str(N)+'&sa=N'

            filename = response.url+'.txt'
            with open('filename','a+') as f:
                f.write('1111')
                f.write(response.body)
            yield Request(url = url,callback = self.parse2,dont_filter=True)
        
        #判断当前页是不是最后一页
        if len(detailurls)==0:#就这样吧，能跑起来就行
            if self.scrawl_ID.__len__():#如果待爬的领域里面还有则继续下一个领域
                field = self.scrawl_ID.pop()
                self.finish_ID.add(field)  # 加入已爬队列
                # field = 'aerospace'
                       # https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
                url = 'https://www.google.com/search?q='+field+'&tbm=pts&start=00'+'&sa=N'
                # yield Request(url=url, callback=self.parse1)
                req = Request(url= url,callback = self.parse1)
                with open('next.txt','a+') as f:
                    f.write(field)
                    f.write('\n')
                yield req
    def parse_info(self,response):
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