#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawler import Crawler
import re

SEED_URL = 'http://blog.sina.com.cn/'

class CrawlerSinaBlog(Crawler):

  def __init__(self):
    self.urls = []

  def getPostUrl(self,seed_url):
    urls = []
    indexPage = self._http_call(seed_url)
    if indexPage:
      while 1:
        pos = indexPage.find('http://blog.sina.com.cn/s/blog_')
        if pos < 0:
          break

        indexPage = indexPage[pos:]
        pos_end = indexPage.find('"')
        if pos_end < 0:
          break
        url = indexPage[:pos_end]
        indexPage = indexPage[pos_end:]
        if url not in self.urls and len(url)>10:
          self.urls.append(url.strip())
        #print url 
    return True
        #self.getPostBody(url)

  def getSeedUrl(self):
    seedUrls = []
    seedUrls.append(SEED_URL)
    indexPage = self._http_call(SEED_URL)
    if indexPage:
      while 1:
        pos = indexPage.find('http://blog.sina.com.cn/lm/')
        if pos < 0:
          break

        indexPage = indexPage[pos:]
        pos_end = indexPage.find('"')
        if pos_end < 0:
          break
        url = indexPage[:pos_end]
        indexPage = indexPage[pos_end:]
        #print url
        if url not in seedUrls and len(url)>10:
          seedUrls.append(url.strip())
        #print url 
    return seedUrls

  def getPostBody(self,url):
    try:
      body = self._http_call(url)
    except:
      return False
    if body:
      pos = body.find('<!--博文正文 begin -->')
      pos_end = body.find('<!--博文正文 end -->')
      content = self.filter_tags(body[pos:pos_end])
      return content

    return False 
      

  def filter_tags(self,htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    s=self.replaceCharEntity(s)#替换实体
    return s

  def replaceCharEntity(self,htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}
    
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
 
  def repalce(self,s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)


#a = crawlerSinaBlog()
#seedUrl = a.getSeedUrl()
#print len(seedUrl)
#if len(seedUrl) > 0:
#  for url in seedUrl:
#    a.getPostUrl(url)
#print len(a.urls)
#a.getPostBody('http://blog.sina.com.cn/s/blog_7c6a1f2c0101ew7x.html?tj=1')
