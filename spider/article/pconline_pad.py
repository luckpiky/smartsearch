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


class ArticlePconlinePad():
    def __init__(self):
        self.url = 'http://pad.pconline.com.cn/reviews/'
        self.content = ""
        self.article_list = []
        self.delay = 0
        self.page = ""
        self.vcodec = "gbk"
        self.site = '太平洋电脑网'
        self.iname = 'androidpad'
        return

    # 获取列表页上的文章标题和url
    # 返回值:newslist   [[title, url]]
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

    # 获取文章页的内容
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
