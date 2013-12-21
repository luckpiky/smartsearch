# coding=utf-8 #

import re
import urllib
import string
import os
import time
import sys
import codecs

from urlparse import *

from BeautifulSoup import * 

from lib.htmlproc import *
from spider.article.a_template import *


class ArticleZolPad(ArticleTemplate):
  site = '中关村在线'
  atype = 'androidpad'

  #find the article list from page
  def findArticleListPage(self, soup):
    return soup.findAll('dl', {'class':'nl_hd clearfix'})

  #parse the one article item that from list, [url, title]
  def parseArticleListItem(self, item_soup):
    item = [unicode(item_soup.dd.h4.a.string), item_soup.dd.h4.a['href']]
    return item

  #find the page
  def findNextPage(self, soup):
    return soup.find('a', {'class':'next'})

  #find next article content page
  def findNextArticlePage(self, soup):
    return soup.find('a', {'class':'bottom'})

  #find article content
  def findArticleContent(self, soup):
    return soup.find('div', {'id':'cotent_idd'})
  




url = ""
class ArticleZolPad1():
    def __init__(self):
        self.url = 'http://pad.zol.com.cn/more/2_1531.shtml'
        self.content = ""
        self.article_list = []
        self.delay = 0
        self.page = ""
        self.vcodec = "gbk"
        self.site = '中关村在线'
        self.iname = 'androidpad'
        return

    # 获取列表页上的文章标题和url
    # 返回值:newslist   [[url, title]]
    def getNewsList(self):
        count = 0
        newslist = []
        soup = BeautifulSoup(self.page)
        tmp1 = soup.findAll('dl', {'class':'nl_hd clearfix'})
        for item in tmp1:
            news = BeautifulSoup(str(item))
            tmp = [unicode(news.dd.h4.a.string), news.dd.h4.a['href']]
            self.article_list.append(tmp)
            newslist.append(tmp)
            count = count + 1
        return newslist


    # 获取下一个列表页
    def getNextPage(self):
        soup = BeautifulSoup(self.page)
        tmp = soup.find('a', {'class':'next'})
        if None != tmp:
            if 'href' != tmp.attrs[0][0]:
                return None
            return tmp.attrs[0][1]
        return None

    # 获取文章页的下一页
    def getNewsContentNextPage(self, page):
        soup = BeautifulSoup(page)
        tmp1 = soup.find('a', {'class':'bottom'})
        if None == tmp1:
            return None
        return urljoin(self.url, tmp1['href'])

    # 获取文章页的内容
    def __getNewsContent(self, url):
        next_url = ""
        content = ""
        page = urllib.urlopen(url).read().decode('gbk')
        soup = BeautifulSoup(page)
        tmp1 = soup.find('div', {'id':'cotent_idd'})

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




