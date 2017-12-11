# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from getpatent.items import GetpatentItem
from scrapy.http import Request
from scrapy.selector import Selector
import time
from random import random
from getpatent.settings import FIELD 

#本来是可以公用的，但多了一个写文件的操作，就不知道怎么处理了
#如果没有写文件的操作，确实是没问题的
def parse_info(response):

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
        rel_patents = list()

        #下面处理patent citations，这是一个引用的表格

        #这是专利的表头
        tablehead = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead//th//text()').extract()

        #这是第一列，Cited Patent
        cited_patent = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*//td/a/text()').extract()
        citedlist = sel.xpath('//span[text()="Patent Citations"]/parent::*/following::*[1]//thead/parent::*//td/a/@href').extract()
        rel_patents = rel_patents + citedlist
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
        rel_patents = rel_patents + citedlist
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
            with open('relpatents.txt','a+') as f:
                for i in rel_patents:
                    if 'http' not in i:
                        url = Url + i
                    f.write(Url+i)
                    f.write('\n')
        yield item