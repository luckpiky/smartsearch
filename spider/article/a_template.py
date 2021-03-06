# coding=utf-8 #

import re
import urllib
import string
import os
import time
import sys
import codecs
from urlparse import *

#thirdparty lib files
from BeautifulSoup import *

#my lib files
from lib.htmlproc import *

class ArticleTemplate():
  url = 'http://url'
  content = ""
  article_list = []
  delay = 0
  page = ""
  vcodec = "gbk"
  site = 'site name'
  atype = 'aritcle type'
  soup = None

  def __init__(self):
    self.article_list = []
    return

  #set self.url
  def setBaseUrl(self, url):
    self.url = url
    return

  #find the article list from page
  def findArticleListPage(self, soup):
    return soup.findAll('dl', {'class':'nl_hd clearfix'})

  #parse the one article item that from list, [url, title]
  def parseArticleListItem(self, item_soup):
    item = [unicode(item_soup.dd.h4.a.string), item_soup.dd.h4.a['href']]
    return item

  # get article list's article's url and title
  # return:article_list [[url, title]]
  def getArticleList(self, cur_url):
    article_lst = []
    page = urllib.urlopen(cur_url).read().decode(self.vcodec)

    #find the list content
    soup = BeautifulSoup(page)
    list_page = self.findArticleListPage(soup)

    #iterate the list and parse the item
    for item_page in list_page:
      try:
        item_soup = BeautifulSoup(str(item_page))
        tmp = self.parseArticleListItem(item_soup)
        if None == tmp:
          continue
        #add to article_list
        article_lst.append(tmp)
      except:
        pass

    return article_lst

  #find the page
  def findNextPage(self, soup):
    return soup.find('a', {'class':'next'})

  #get next page for article list
  def getNextListPage(self, cur_url):
    url = ""
    page = urllib.urlopen(cur_url).read().decode(self.vcodec)
    soup = BeautifulSoup(page)
    tmp = self.findNextPage(soup)
    if None != tmp:
      if 'href' != tmp.attrs[0][0]:
        return None
      url = tmp.attrs[0][1]
    else:
      return None
    return url

  #find next article content page
  def findNextArticlePage(self, soup):
    return soup.find('a', {'class':'bottom'})

  #get next page for article content
  def getNextArticlePage(self, url, page):
    soup = BeautifulSoup(page)
    tmp = self.findNextArticlePage(soup)
    if None == tmp:
      return None
    return urljoin(url, tmp['href'])    

  #find article content
  def findArticleContent(self, soup):
    return soup.find('div', {'id':'cotent_idd'})

  def formatContent(self, content):
    return getPNode(content)

  #get article content
  def getArticleContent(self, url):
    next_url = ""
    content = ""
    page = urllib.urlopen(url).read().decode(self.vcodec)
    soup = BeautifulSoup(page)
    tmp1 = self.findArticleContent(soup)

    if None == tmp1:
      return None

    next_url = self.getNextArticlePage(url, page)
    if None != next_url and '' != next_url:
      print 'read content url:',next_url
      content_tmp = self.getArticleContent(next_url)
      if None != content_tmp:
        content = content + content_tmp
    if None != tmp1 and '' != tmp1:
      content = tmp1.__str__() + content

    return self.formatContent(content)





