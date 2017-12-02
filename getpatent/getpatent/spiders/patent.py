# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from getpatent.items import GetpatentItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random


'''
aerospace第五页
https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
Biomedical engineering空格不用加下滑线

'''

Url = 'https://www.google.com'

    
class ScholarSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['www.google.ca','www.google.com']
    start_urls=['aerospace']
    #处理start_urls=[]
    # keys = ['aerospace']#之后可以添加
    # # keys = ['bigdata']
    # # keys = ['biology']
    # # # keys = ['infornet']
    # # keys = ['newM']
    # # keys = ['QC']
    # # keys = ['shipB']
    
    # for key in keys:
    #     file_ = 'new/'+key+'.txt'
    #     with open(file_,'r') as f:
    #         list_ = f.readlines()
    #         for i in list_:
    #             start_urls.append(i)
    #             if ' ' in i:
    #                 i=i.replace(' ','_')
    #                 start_urls.append(i)#也就是说有下划线，没下划线的都要

    # keys = ['aerospace']#之后可以添加
    # # keys = ['bigData']
    # # keys = ['biology']
    # # keys = ['informationNetworks']
    # # keys = ['newMaterials']
    # # keys = ['QuantumCommunication']
    # # keys = ['shipBuilding']
    
    # for key in keys:
    #     file_ = 'key/'+key+'.txt'
    #     with open(file_,'r') as f:
    #         list_ = f.readlines()
    #         for i in list_:
    #             start_urls.append(i)
    #             if ' ' in i:
    #                 i=i.replace(' ','_') 
    #                 start_urls.append(i)#也就是说有下划线，没下划线的都要

    scrawl_ID = set(start_urls)  # 记录待爬
    finish_ID = set()  # 记录已爬
    peopleUrl = set() #记录已经爬的主页

    def start_requests(self):

        while self.scrawl_ID.__len__():
            print self.scrawl_ID.__len__()
            field = self.scrawl_ID.pop()
            self.finish_ID.add(field)  # 加入已爬队列
            # field = 'aerospace'
                   # https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
            url = 'https://www.google.com/search?q='+field+'&tbm=pts&start=00'
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
            req = Request(url,callback = self.parse_info,dont_filter=True)
            reqs.append(req)
            # yield Request(url = url,callback = self.parse_info,dont_filter=True)
        # yield reqs    
        # nexturl = sel.xpath('//*[text()="Next"]/parent::*/@href').extract()
        # nexturl2 = sel.xpath('//*[text()="Next"]/@href').extract()
        # nexturl_1= response.xpath('//*[@class="b"]/a/@href').extract()
        # nexturl_2 = response.xpath('//*[@class="b navend"]/a/@href').extract()
        # print('---------------111--------------',nexturl)
        # print('-----------3----------------',nexturl_1)
        # print('-----------3----------------',nexturl_2)

        # if nexturl:
        #     if nexturl:
        #         url = nexturl[0]
        #         yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        # elif len(nexturl2)==1:
        #     print('-------------222---------------',nexturl2)
        #     if nexturl2:
        #         url = nexturl2[0]
        #         yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        # elif len(nexturl_1)==2:
        #     print('-----------3----------------',nexturl_1)
        #     url = nexturl_1[1]
        #     yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        # elif len(nexturl_2)==2: 
        #     print('-----------4444----------------',nexturl_2)
        #     url = nexturl_2[1]
        #     yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        # elif len(nexturl_2)==2: 
        #     print('-----------4444----------------',nexturl_2)
        #     url = nexturl_2[1]
        #     yield Request(url = Url+url,callback = self.parse1,dont_filter=True)
        if len(detailurls) ==10:
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
         
            nexturl = 'https://www.google.com.hk/search?q='+key+'&tbm=pts&start='+str(N)
            req =  Request(url = nexturl,callback = self.parse1,dont_filter=True)
            reqs.append(req)
            # yield Request(url = url,callback = self.parse_info,dont_filter=True)
        for req in reqs:
            yield req
            # with open('./worng_html.txt','w+') as f:
            #     f.write('1111')
            #     f.write(response.body)

  

    def parse_info(self, response):

        '''
        再加一个字段把当前url存下来
        '''
        item = GetpatentItem()
        sel = Selector(response)
        title = sel.xpath('//span[@class="patent-title"]//invention-title/text()').extract()
        
#         print response.url
        
#         item['Url'] = response.url

#         if title:
#             item['Title'] = title[0]
#         else:
#             item['Title'] = ''
#         abstract =sel.xpath('//*[text()="Abstract"]/parent::*/following-sibling::*//text()').extract()
#         if abstract:
#             item['Abstract'] = abstract[0]
#         else:
#             item['Abstract'] = ''
        

#         #右边卡片中的信息
        now = sel.xpath('//*[text()="Publication number"]/following::*[1]/text()').extract()
        if now:
            item['Publication_number'] = now[0]
        else:
            item['Publication_number'] = ''
        yield item
#         now = sel.xpath('//*[text()="Publication type"]/following::*[1]/text()').extract()
#         if now:
#             item['Publication_type'] = now[0]
#         else:
#             item['Publication_type'] = ''

#         now = sel.xpath('//*[text()="Publication date"]/following::*[1]/text()').extract()
#         if now:
#             item['Publication_date'] = now[0]
#         else:
#             item['Publication_date'] = ''

#         now = sel.xpath('//*[text()="Original Assignee"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
#         if now:
#             item['Original_Assignee'] = now[0]
#         else:
#             item['Original_Assignee'] = ''

#         now = sel.xpath('//*[text()="Filing date"]/following::*[1]/text()').extract()
#         if now:
#             item['Filing_date'] = now[0]
#         else:
#             item['Filing_date'] = ''

#         now = sel.xpath('//*[text()="Application number"]/following::*[1]/text()').extract()
#         if now:
#             item['Application_number'] = now[0]
#         else:
#             item['Application_number'] = ''

#         now = sel.xpath('//*[text()="Priority date"]/following::*[1]/text()').extract()
#         if now:
#             item['Priority_date'] = now[0]
#         else:
#             item['Priority_date'] = ''
        
#         now = sel.xpath('//*[text()="Inventors"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
#         if now:
#             item['Inventors'] = now
#         else:
#             item["Inventors"] = ''

#         now = sel.xpath('//*[text()="Applicant"]/following::*[1]/text()').extract()
#         if now:
#             item['Applicant'] = now[0]
#         else:
#             item['Applicant'] = ''

#         now = sel.xpath('//*[text()="Export Citation"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        
#         if now:
#             item['Export_Citation'] = now
#         else:
#             item["Export_Citation"] = ''

#         now = sel.xpath('//*[text()="Also published as"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        
#         if now:
#             item['Also_published_as'] = now
#         else:
#             item["Also_published_as"] = ''
#         #额外的参考链接
#         url = sel.xpath('//td[@colspan="2"]/span[@class="patent-bibdata-heading"]/parent::*//*[@class="patent-bibdata-value"]//a/@href').extract()
#         site = sel.xpath('//td[@colspan="2"]/span[@class="patent-bibdata-heading"]/parent::*//*[@class="patent-bibdata-value"]//a/text()').extract()
#         if now:
#             d = dict()
#             for i in range(len(site)):
#                 if url[i]:
#                     d[site[i]] = url[i]
#                 else:
#                     d[site[i]] = ''
#             item['External_Links'] = d
#         else:
#             item['External_Links'] = ''

        
#         '''
#         不要描述信息，不然太多了
#         '''
#         #下面处理patent citations，这是一个引用的表格

#         #这是专利的表头
#         tablehead = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead//th//text()').extract()
#         #这是第一列，Cited Patent
#         cited_patent = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*//td/a/text()').extract()
#         #这是第二列第三列[col2,col3,col2,co3.....]
#         stclo = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td patent-date-value"]//text()').extract()
#         #这是第四列第五列
#         ffclo =  sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td "]//text()').extract()
#         #下面就是把这四项合成一个表格了
# #'https://www.google.com/patents/US8720825?dq=aerospace&hl=en&sa=X&ved=0ahUKEwib9M3io-bXAhWqsVQKHUoTBcsQ6AEIKDAA'
#         #怎么和
#         if tablehead:
#             seccol = stclo[0::2]
#             thirdcol = stclo[1::2]
#             fifcol = ffclo[0::2]
#             fivcol = ffclo[1::2]
#             print tablehead
#             d = {
#                 tablehead[0]:cited_patent,
#                 tablehead[1]:seccol,
#                 tablehead[2]:thirdcol,
#                 tablehead[3]:fifcol,
#                 tablehead[4]:fivcol
#             }
#             # print d
#             # table = DataFrame(d)
#             # print table
#             item['Cited_patent'] = d
#         else:
#             item['Cited_patent'] = ''


#         #下面处理REFERENCED BY  
#         #这是专利的表头
#         tablehead = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead//th//text()').extract()
#         #这是第一列，Cited Patent
#         cited_patent = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*//td/a/text()').extract()
#         #这是第二列第三列[col2,col3,col2,co3.....]
#         stclo = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td patent-date-value"]//text()').extract()
#         #这是第四列第五列
#         ffclo =  sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td "]//text()').extract()
#         #下面就是把这四项合成一个表格了
# #'https://www.google.com/patents/US8720825?dq=aerospace&hl=en&sa=X&ved=0ahUKEwib9M3io-bXAhWqsVQKHUoTBcsQ6AEIKDAA'
#         #怎么和
#         if tablehead:
#             seccol = stclo[0::2]
#             thirdcol = stclo[1::2]
#             fifcol = ffclo[0::2]
#             fivcol = ffclo[1::2]
#             print tablehead
#             d = {
#                 tablehead[0]:cited_patent,
#                 tablehead[1]:seccol,
#                 tablehead[2]:thirdcol,
#                 tablehead[3]:fifcol,
#                 tablehead[4]:fivcol
#             }
#             # print d
#             # table = DataFrame(d)
#             # print table
#             item['Referenced_by'] = d
#         else:
#             item['Referenced_by'] = ''



        '''
        1.分类的那个表格
        2.把referenced 和 cited_patent 的链接写入文件
        3.继续构造像人才那样的三到四级爬取


        '''


       # yield item