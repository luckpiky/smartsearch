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

#reload(sys)
#sys.setdefaultencoding('gbk')

url = "http://pad.zol.com.cn/389/3898084.html"

def formatUrl1(content, url):
    urls = []
    soup = BeautifulSoup(content)
    tmp1 = soup.findAll('a')
    if None == tmp1:
        return
    for tmp2 in tmp1:
        try:
            can_add = True
            for urltmp in urls:
                if urltmp == tmp2['href']:
                    can_add = False
                    break
            if can_add:
                urls.append(tmp2['href'])
        except:
            pass
    #reload(sys)
    #sys.setdefaultencoding('gbk')
    for tmp3 in urls:
        urltmp = urljoin(url, tmp3)
        content = content.replace(tmp3, urltmp)
    return content


#去除文本中的链接
def removeUrls1(self, content):
    content = content.decode('gbk')
    soup = BeautifulSoup(content)
    tmp1 = soup.findAll('a')
    [tmp2.extract() for tmp2 in tmp1]
    return soup.renderContents()



# test
#page = getNewsContent('http://pad.zol.com.cn/389/3898084.html')
#fp = open('d:/aa.html', 'w')
#fp.write(page)
#fp.close()

def getBaseInfo():
    page_index = 1
    url = 'http://pad.zol.com.cn/more/2_1531.shtml'
    while(url!=None):
        page = urllib.urlopen(url).read().decode('gbk')
        tmp = getNextPage(page)
	print 'next:',tmp
	if None != tmp:
            url = urljoin(url, tmp)
            page_index = page_index + 1
        else:
            url = None
        newlist = getNewsList(page)
        for  t in newlist:
            print t[0],t[1]
        time.sleep(1)
    return
    page = urllib.urlopen(url).read().decode('gbk')
    soup = BeautifulSoup(page)
    newslist = soup.findAll('dl', {'class' : 'nl_hd clearfix'})
    for item in newslist:
        soup2 = BeautifulSoup(str(item))
	print soup2.dd.h4.a['href']
        title = soup2.find('a')
	if None != title:
            print title.attrs[0][1], title.string
    return



class ArticleZolPad():
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
