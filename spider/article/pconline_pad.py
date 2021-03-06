# coding=utf-8 #

import re
import urllib
import string
import os
import time
import sys
import codecs

from BeautifulSoup import * 

from lib.htmlproc import *
from spider.article.a_template import *

class ArticlePconlinePad(ArticleTemplate):
  site = '太平洋电脑网'
  atype = 'androidpad'

  #find the article list from page
  def findArticleListPage(self, soup):
    return soup.findAll('li')

  #parse the one article item that from list, [url, title]
  def parseArticleListItem(self, item_soup):
    item = [unicode(item_soup.dl.dt.a.string), item_soup.dl.dt.a['href']]
    return item

  #find the page
  def findNextPage(self, soup):
    return soup.find('a', {'class':'next'})

  #find next article content page
  def findNextArticlePage(self, soup):
    tmp1 = soup.find('div', {'class':'pconline_page pageLast'})
    if None == tmp1:
      return None
    try:
      page = tmp1.__str__() 
      soup1 = BeautifulSoup(page)      
      return soup1.find('a', {'class':'next'})
    except:
      return None

  #find article content
  def findArticleContent(self, soup):
    return soup.find('div', {'class':'content'})


#t = pconline1()
#t.setBaseUrl("http://pad.pconline.com.cn/reviews/")
#t.page = urllib.urlopen(t.url).read().decode(t.vcodec)
#lst1 = t.getArticleList()
#urlt = ""
#for t1 in lst1:
  #print t1[0],t1[1]
#  urlt = t1[1]
#print urlt
#con = t.getArticleContent("http://pad.pconline.com.cn/372/3724861.html")
#print con



class ArticlePconlinePad1():
    def __init__(self):
        self.url = 'http://pad.pconline.com.cn/reviews/'
        self.content = ""
        self.article_list = []
        self.delay = 0
        self.page = ""
        self.vcodec = "gbk"
        self.site = '̫ƽ????????'
        self.iname = 'androidpad'
        return

    # ??ȡ?б?ҳ?ϵ????±?????url
    # ????ֵ:newslist   [[title, url]]
    def getNewsList(self):
        count = 0
        newslist = []
        soup = BeautifulSoup(self.page)
        tmp1 = soup.findAll('li')
        for item in tmp1:
            try:
                news = BeautifulSoup(str(item))
                tmp = [unicode(news.dl.dt.a.string), news.dl.dt.a['href']]
                self.article_list.append(tmp)
                newslist.append(tmp)
                count = count + 1
            except:
                pass
        return newslist

    # ??ȡ??һ???б?ҳ
    def getNextPage(self):
        soup = BeautifulSoup(self.page)
        tmp = soup.find('a', {'class':'next'})
        if None != tmp:
            if 'href' != tmp.attrs[0][0]:
                return None
            return tmp.attrs[0][1]
        return None

    # ??ȡ????ҳ????һҳ
    def getNewsContentNextPage(self, page):
        soup = BeautifulSoup(page)
        tmp1 = soup.find('div', {'class':'pconline_page pageLast'})
        if None == tmp1:
            return None
        try:
            page = tmp1.__str__() 
            soup1 = BeautifulSoup(page)
            
            tmp1 = soup1.find('a', {'class':'next'})
            if None == tmp1:
                return None
            return urljoin(self.url, tmp1['href'])
        except:
            return None
        return None

    # ??ȡ????ҳ??????
    def __getNewsContent(self, url):
        next_url = ""
        content = ""
        page = urllib.urlopen(url).read().decode(self.vcodec)
        soup = BeautifulSoup(page)
        tmp1 = soup.find('div', {'class':'content'})

        if None == tmp1:
            return None

        next_url = self.getNewsContentNextPage(page)
        if None != next_url and '' != next_url:
            print 'read content url:',next_url
            content = content + self.getNewsContent(next_url)
            #content = formatUrl(tmp1.__str__('gbk'), url) + content
        #content = removeUrls(tmp1.__str__('gbk')) + content
        if None != tmp1 and '' != tmp1:
            content = tmp1.__str__() + content
            #return tmp1.__str__('gbk')
        return content

    def getNewsContent(self, url):
        content = self.__getNewsContent(url)
        content = getPNode(content)
        content = removeUrls(content)
        content = formatImg(content)
        return content
