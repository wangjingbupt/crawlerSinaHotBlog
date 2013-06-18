#!/usr/bin/python
# encoding=utf8 
import sys,time
sys.path.append("./crawler")
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerSinaBlog import CrawlerSinaBlog
from  datetime  import  * 

import pymongo,time

host = '127.0.0.1'
port = 27017
conn = pymongo.Connection(host, port)
print '------------------'
print datetime.today()

a = CrawlerSinaBlog()
seedUrl = a.getSeedUrl()
print len(seedUrl)
if len(seedUrl) > 0:
  for url in seedUrl:
    a.getPostUrl(url)
print len(a.urls)
if len(a.urls) > 0 :
  count = 1
  for url in a.urls:
    pos = url.find('http://blog.sina.com.cn/s/blog_')
    if pos < 0:
      continue
    pos +=31
    pos_end = pos + url[pos:].find('.') 
    blogId = url[pos:pos_end]
    s = conn.blog.post.find_one({'blogId':blogId})
    if not s:
      body = a.getPostBody(url)
      doc = {'blogId':blogId,'content':body}
      conn.blog.post.insert(doc)
      count += 1
    if count % 20 == 0:
      time.sleep(5)

    #print body
print (count-1)
print datetime.today()
print ''
