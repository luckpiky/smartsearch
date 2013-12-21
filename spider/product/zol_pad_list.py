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
from spider.models import *
from lib.smartscript import *


system_list = ['iOS', 'Windows', 'Android', 'Linux']
company_list = SmtCompany.objects.all()


def get_str_by_soup(soup):
    node = soup
    while None != node:
        if None != node.string:
            return node.string
            break
        node = node.next


class ProductZolPad(ArticleTemplate):
  site = '中关村在线'
  atype = 'andoridpad'

  #find the article list from page
  def findArticleListPage(self, soup):
    return soup.findAll('div',{'class':'pro-intro'})

  #parse the one article item that from list, [url, title]
  def parseArticleListItem(self, item_soup):
    #print item_soup
    print item_soup.h3.a.string
    t = item_soup.find('a', {'class':'more'})
    print t['href']
    item = [unicode(item_soup.h3.a.string), t['href']]
    return item

  #find the page
  def findNextPage(self, soup):
    return soup.find('a', {'class':'next'})

  #find next article content page
  def findNextArticlePage(self, soup):
    return None

  #find article content
  def findArticleContent(self, soup):
    return None
  
  #get article content
  def getArticleContent(self, name, url):
    page = urllib.urlopen(url).read().decode(self.vcodec)
    if None == page or '' == page:
      return None
    soup = BeautifulSoup(page)
    product = SmtProductPad()

    product.url = url

    name = name.strip() #去除空格
    print 'name:', name
    product.fullname = name
    for company_s in company_list:
        company = company_s.name
        product.company_id = company_s.id
        if -1 != name.find(company):
            print 'company:',company
            i_type = name.find('（')
            if -1 != i_type:
                print 'name:',name[len(company):i_type].strip()
                print 'type:',name[i_type:]
                product.name = name[len(company):i_type].strip()
                product.nametype = name[i_type:].strip()
            else:
                print 'name:',name[len(company):]
                product.name = name[len(company):].strip()

    for i in range(1,10):
      value_key = 'oldPmVal_' + str(i)
      name_key = 'oldPmName_' + str(i)
      t = soup.find('span', {'id':value_key})
      t2 = soup.find('th', {'id':name_key})
      if None == t or '' == t or None == t2 or '' == t2:
        print "NONE"
        continue
      #print name_key, get_str_by_soup(t2)
      #print value_key,get_str_by_soup(t)
      value = get_str_by_soup(t).strip()
      name = get_str_by_soup(t2).strip()
      if '上市时间' == name:
          print name,value
          product.saletime = value
      if '操作系统' == name:
          print name,value
          for system_name in system_list:
              if -1 !=  value.find(system_name):
                  print 'system:',system_name
                  product.system = system_name
                  if len(value) > len(system_name):
                      product.system_version = value[len(system_name):(len(value))].strip()
                      print 'system_version:',product.system_version
      if '处理器型号' == name:
          print name,value
          product.cpu = value
      if '处理器核心' == name:
          print name,value
          product.cpucores = value
      if '处理器主频' == name:
          print name,value
          product.cpu_frequency = value
      if '显卡核心' == name:
          print name,value
          product.gpucores = value
      if '系统内存' == name:
          print name,value
          product.memory = value
      if '存储容量' == name:
          print name,value
          product.storage = value
      if '存储扩展' == name:
          print name,value
          product.storage_ext = value
      if '屏幕尺寸' == name:
          print name,value
          product.screen_size = value
      if '屏幕分辨率' == name:
          print name,value
          product.screen_resolution = value
      if '屏幕像素密度' == name:
          print name,value
          product.screen_ppi = value
      if '屏幕特性' == name:
          print name,value
          product.screen_character = value
      if '摄像头' == name:
          print name,value
          product.camera = value
      if '续航时间' == name:
          print name,value
          product.battery_life = value
      if '产品尺寸' == name:
          print name,value
          product.size = value
      if '产品重量' == name:
          print name,value
          product.weight = value
    
    product.save_to_db()

    return None
      






