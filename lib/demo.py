#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("./crawler")
from crawlerSinaBlog import CrawlerSinaBlog

import pymongo

a = CrawlerSinaBlog()
seedUrl = a.getSeedUrl()
print len(seedUrl)
if len(seedUrl) > 0:
  for url in seedUrl:
    a.getPostUrl(url)
print len(a.urls)
if len(a.urls) > 0 :
  for url in a.urls:
    body = a.getPostBody(url)
    print body
    sys.exit()
