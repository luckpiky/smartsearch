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

class ArticleCnmoPad(ArticleTemplate):
  site = '手机中国'
  atype = 'androidpad'
  vcodec = 'gbk'

  #find the article list from page
  def findArticleListPage(self, soup):
    t = soup.find('div', {'class':'cc_mem'})
    if None == t:
      return None
    page = t.__str__()
    soup1 = BeautifulSoup(page)
    return soup1.findAll('li')

  #parse the one article item that from list, [url, title]
  def parseArticleListItem(self, item_soup):
    item_soup = item_soup.find('a',{'class':'lan'})
    item = [unicode(item_soup.string), item_soup['href']]
    return item

  #find the page
  def findNextPage(self, soup):
    return soup.find('a', {'class':'prev'})

  #find next article content page
  def findNextArticlePage(self, soup):
    tmp1 = soup.find('div', {'id':'page_num'})
    if None == tmp1:
      return None
    try:
      tmp1 = tmp1.findAll('a')
      t = tmp1[len(tmp1)-1]
      href = t['href']
      return t
    except:
      return None

  #find article content
  def findArticleContent(self, soup):
    return soup.find('div', {'class':'art_nr'})


