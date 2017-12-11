import sys  
import os  
import time  
from scrapy.cmdline import execute  
import os  
os.system("scrapy crawl patent")  
time.sleep(20)  
os.system("scrapy crawl patent2")
time.sleep(20)
os.system("scrapy crawl patent3")
time.sleep(20)
os.system("scrapy crawl patent4")