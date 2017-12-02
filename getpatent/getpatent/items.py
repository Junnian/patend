# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class GetpatentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Url = Field()
    Title = Field()     #专利名称
    Category = Field()  #分类  # 专利类型  /发布类型  待定
    Country = Field()   #所属地域   /从专利号里截取
    PatentNumber = Field()   #专利号   /就是题目下边的号
    ApplicaDay = Field()  # 申请时间  /申请日期
    Publicday = Field()  # 授权时间  /公开日
    
    # InverAff = Field() #发明单位  /没有 啊
    Abstract = Field()  #摘要
    Keywords = Field()  #关键词
    # PatentApplicaN = Field() #专利申请号
    #
    #
    #
    # Noticeumber = Field() #公告号
    #
    # Orissignee = Field()#原受让人
    # Reference = Field() #引用别人
    # Ref_num = Field()#引用别人专利的数量
    # Cited = Field() #被谁应用
    # Cited_num = Field()#被引用的数量
    # Category = Field() #分类
    Publication_number = Field()
    Publication_type = Field()
    Application_number = Field()
    Publication_date = Field()
    Applicant = Field()
    Filing_date = Field()
    Priority_date = Field()
    Original_Assignee = Field()
    Export_Citation = Field()
    Also_published_as = Field()
    Inventors = Field()  # 发明人 V
    External_Links = Field()

    Cited_patent = Field()#是一个dict形式的表格，或字符串
    Referenced_by = Field()
    pass
