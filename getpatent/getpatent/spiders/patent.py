# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from getpatent.items import GetpatentItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random
from getpatent.settings import FIELD 
# from getpatent.spiders.parse_info import parse_info

'''
aerospace第五页
https://www.google.com.hk/search?q=aerospace&tbm=pts&start=40
Biomedical engineering空格不用加下滑线

'''

Url = 'https://www.google.com'

outfilename = 'relpatents.txt' 
class ScholarSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['www.google.ca','www.google.com']
    start_urls=[]
    
    
    if FIELD==0:
        key1s = ['test'] #new
        key2s = ['test'] #key
    if FIELD==1:
        key1s = ['aerospace'] #new
        key2s = ['aerospace'] #key
    if FIELD==2:
        key1s = ['bigdata']
        key2s = ['bigData','bigData2','big_data']
    if FIELD==3:
        key1s = ['infornet']
        key2s = ['informationNetworks']
    if FIELD==4:
        key1s = ['newM']
        key2s = ['newMaterials']
    if FIELD==5:
        key1s = ['QC']
        key2s = ['quantumCommunication']
    if FIELD==6:
        key1s = ['ShipB']
        key2s = ['shipBuilding']
    if FIELD==7:
        key1s = ['biology']
        key2s = ['biology','Biological Engineering']

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

        '''
        再加一个字段把当前url存下来
        '''
        item = GetpatentItem()
        sel = Selector(response)
        title = sel.xpath('//span[@class="patent-title"]//invention-title/text()').extract()
        
        # print response.url
        
        item['Url'] = response.url

        if title:
            item['Title'] = title[0]
        else:
            item['Title'] = ''
        abstract =sel.xpath('//*[text()="Abstract"]/parent::*/following-sibling::*//text()').extract()
        if abstract:
            item['Abstract'] = abstract[0]
        else:
            item['Abstract'] = ''
        

#         #右边卡片中的信息
        now = sel.xpath('//*[text()="Publication number"]/following::*[1]/text()').extract()
        if now:
            item['Publication_number'] = now[0]
        else:
            item['Publication_number'] = ''
        # yield item
        now = sel.xpath('//*[text()="Publication type"]/following::*[1]/text()').extract()
        if now:
            item['Publication_type'] = now[0]
        else:
            item['Publication_type'] = ''

        now = sel.xpath('//*[text()="Publication date"]/following::*[1]/text()').extract()
        if now:
            item['Publication_date'] = now[0]
        else:
            item['Publication_date'] = ''

        now = sel.xpath('//*[text()="Original Assignee"]/parent::*//span[@class="patent-bibdata-value-list"]/span//a//text()').extract()
        if now:
            item['Original_Assignee'] = now[0]
        else:
            item['Original_Assignee'] = ''

        now = sel.xpath('//*[text()="Filing date"]/following::*[1]/text()').extract()
        if now:
            item['Filing_date'] = now[0]
        else:
            item['Filing_date'] = ''

        now = sel.xpath('//*[text()="Application number"]/following::*[1]/text()').extract()
        if now:
            item['Application_number'] = now[0]
        else:
            item['Application_number'] = ''

        now = sel.xpath('//*[text()="Priority date"]/following::*[1]/text()').extract()
        if now:
            item['Priority_date'] = now[0]
        else:
            item['Priority_date'] = ''
        
        now = sel.xpath('//*[text()="Inventors"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        if now:
            item['Inventors'] = now
        else:
            item["Inventors"] = ''

        now = sel.xpath('//*[text()="Applicant"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        if now:
            item['Applicant'] = now[0]
        else:
            item['Applicant'] = ''

        now = sel.xpath('//*[text()="Export Citation"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        
        if now:
            item['Export_Citation'] = now
        else:
            item["Export_Citation"] = ''

        now = sel.xpath('//*[text()="Also published as"]/parent::*//span[@class="patent-bibdata-value-list"]/span/a//text()').extract()
        
        if now:
            item['Also_published_as'] = now
        else:
            item["Also_published_as"] = ''
        #额外的参考链接
        url = sel.xpath('//td[@colspan="2"]/span[@class="patent-bibdata-heading"]/parent::*//*[@class="patent-bibdata-value"]//a/@href').extract()
        site = sel.xpath('//td[@colspan="2"]/span[@class="patent-bibdata-heading"]/parent::*//*[@class="patent-bibdata-value"]//a/text()').extract()
        if now:
            d = dict()
            for i in range(len(site)):
                if url[i]:
                    d[site[i]] = url[i]
                else:
                    d[site[i]] = ''
            item['External_Links'] = d
        else:
            item['External_Links'] = ''

        
        #下面处理表格：新建一个引用或被引用的list,修后见这个list写在文件里，供深入爬取使用
        rel_patents = set()

        #下面处理patent citations，这是一个引用的表格

        #这是专利的表头
        tablehead = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead//th//text()').extract()

        #这是第一列，Cited Patent
        cited_patent = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*//td/a/text()').extract()
        citedlist = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*//td/a/@href').extract()
        for i in range(len(citedlist)):
            rel_patents.add(citedlist[i])
          # 这是第二列第三列[col2,col3,col2,co3.....]
        stclo = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td patent-date-value"]//text()').extract()
        #这是第四列第五列
        ffclo =  sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td "]//text()').extract()
        #下面就是把这四项合成一个表格了
#'https://www.google.com/patents/US8720825?dq=aerospace&hl=en&sa=X&ved=0ahUKEwib9M3io-bXAhWqsVQKHUoTBcsQ6AEIKDAA'
        #怎么和
        if tablehead:
            seccol = stclo[0::2]
            thirdcol = stclo[1::2]
            fifcol = ffclo[0::2]
            fivcol = ffclo[1::2]
            # print tablehead
            d = {
                tablehead[0]:cited_patent,
                tablehead[1]:seccol,
                tablehead[2]:thirdcol,
                tablehead[3]:fifcol,
                tablehead[4]:fivcol
            }
            # print d
            # table = DataFrame(d)
            # print table
            item['Cited_patent'] = d
        else:
            item['Cited_patent'] = ''


        #下面处理REFERENCED BY  
        #这是专利的表头
        tablehead = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead//th//text()').extract()
        #这是第一列，Cited Patent
        cited_patent = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*//td/a/text()').extract()
        cited_patent = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*//td/a/@href').extract()
        for i in range(len(citedlist)):
            rel_patents.add(citedlist[i])
        #这是第二列第三列[col2,col3,col2,co3.....]
        stclo = sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td patent-date-value"]//text()').extract()
        #这是第四列第五列
        ffclo =  sel.xpath('//span[text()="Referenced by"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td "]//text()').extract()
        #下面就是把这四项合成一个表格了
#'https://www.google.com/patents/US8720825?dq=aerospace&hl=en&sa=X&ved=0ahUKEwib9M3io-bXAhWqsVQKHUoTBcsQ6AEIKDAA'
        #怎么和
        if tablehead:
            seccol = stclo[0::2]
            thirdcol = stclo[1::2]
            fifcol = ffclo[0::2]
            fivcol = ffclo[1::2]
            # print tablehead
            d = {
                tablehead[0]:cited_patent,
                tablehead[1]:seccol,
                tablehead[2]:thirdcol,
                tablehead[3]:fifcol,
                tablehead[4]:fivcol
            }
            # print d
            # table = DataFrame(d)
            # print table
            item['Referenced_by'] = d
        else:
            item['Referenced_by'] = ''

            #下面处理Classifications那个表

            #这个表格处理的难点是，1，行数不固定，2，参数不固定，所以就不知道怎么存

        # 第一列
        cs = sel.xpath('//span[text()="Classifications"]/parent::*/following::*[1]//thead/parent::*[1]//td[@class="patent-data-table-td "][1]//text()').extract()
        # print('********************',cs)
        d = dict()
        item['Classification'] = ''
        if len(cs):
            for i in range(len(cs)):
                if cs[i] == "U.S. Classification":
                    a = sel.xpath('//td[text()="U.S. Classification"]/parent::*/td[@class="patent-data-table-td "]/span//text()').extract()
                    d[cs[i].replace('.',' ')] = a
                elif cs[i] == "International Classification":
                    a = sel.xpath('//td[text()="International Classification"]/parent::*/td[@class="patent-data-table-td "]/span//text()').extract()
                    d[cs[i]] = a
                elif cs[i] == "Cooperative Classification":
                    a = sel.xpath('//td[text()="Cooperative Classification"]/parent::*/td[@class="patent-data-table-td "]/span//text()').extract()
                    d[cs[i]] = a
                elif cs[i] == "European Classification":
                    a = sel.xpath('//td[text()="European Classification"]/parent::*/td[@class="patent-data-table-td "]/span//text()').extract()
                    d[cs[i]] = a
                else:
                    #测试用，要是遇到没见过的分类就写在文件里，后补充，xpath修改上边的text即可
                    with open('otherclass.txt','a+') as f:
                        f.write(cs[i])
                        f.write('\n')
       
            item['Classification'] = d
          
        #写下相关联的专利       
        with open(outfilename,'a+') as f:
            # for i in rel_patents:
            #     if 'http' not in i:
            #         url = Url + i
            #     f.write(Url+i)
            #     f.write('\n')
            while rel_patents.__len__():
                url = rel_patents.pop()
                if 'http' not in url:
                    url = Url + url
                if '/patents/' in url:
                    f.write(url)
                    f.write('\n')
        yield item