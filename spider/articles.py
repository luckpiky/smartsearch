# coding=utf-8 #

import urllib
import string
import os
import time
from spider.models import *
from spider.article.zol_pad import *
from spider.article.pconline_pad import *

reload(sys)
sys.setdefaultencoding('utf-8')

class Article():
  def __init__(self):
    self.node_list = []
    self.MAX_READ_PERNODE = 25
    self.MAX_DESCRIPTION = 100
    return

  def writeArticle(self, title, url, content, node):
    article = SmtArticle()
   
    article.title = title.encode('utf-8' )
    article.url = url
    article.content = removeScript(content)
    article.site = node.site.decode('gbk')
    article.pic = getFirstPicture(content)
    article.description = getContentDescription(article.content, self.MAX_DESCRIPTION)
    article.save()

    return True

  def checkArticleExist(self, title, url):
    title = title.encode('utf-8')
    rst = SmtArticle.objects.filter(title=title)
    if None != rst and len(rst) > 0:
        return False
    rst = SmtArticle.objects.filter(url=url)
    if None != rst and len(rst) > 0:
        return False
    return True

  def getArticle(self, node):
    # while read articlelist and next page url
    page_index = 1
    count = 0
    while(None != node.url):
      url = node.url
      print 'urllib read:',url
      node.page = urllib.urlopen(url).read().decode(node.vcodec)
      
      #print node.page
      tmp = node.getNextPage()
      if None != tmp:
        node.url = urljoin(url, tmp)
        print node.url
        page_index = page_index + 1
      else:
        node.url = None
      newslist = node.getNewsList()
      print 'read ' + str(len(newslist)) + ' articles'

      # read aritcle content
      for article in newslist:
        print article[0],article[1] # title url
        
        #control the count
        count = count + 1
        if count > self.MAX_READ_PERNODE:
            return

        # check and read and write a article
        if self.checkArticleExist(article[0], article[1]):
          content = node.getNewsContent(article[1])

          # write to file
          if None != content and '' != content:
            self.writeArticle(article[0], article[1], content, node)      
          continue
    return

  def getArticles(self):
    for node in self.node_list:
      self.getArticle(node[1])
    return

  def register(self, name, node):
    has = False
    for t in self.node_list:
      if t[0] == name:
        has = True
        break
    if False == has:
      self.node_list.append([name, node()])
    return

class ArticleHtmlProc():
  def __init__(self):
    self.COUNT_PER_PAGE = 10
    return

  def createListPage(self):
    c = 0
    page = 1
    rst = SmtArticle.objects.order_by("-id").all()
    for item in rst:
      if 0 == c:
        print "page ",page,":"
      print item.id,item.title
      c = c + 1
      if c == self.COUNT_PER_PAGE:
        c = 0
        page = page + 1
    return

  def createContentPage(self):
    rst = SmtArticle.objects.all()
    for item in rst:
      print item.id,item.title
    return


def get_articles():
  print "get articles"
  a = Article()
  a.register('zolpad', ArticleZolPad)
  a.register('pconlinepad', ArticlePconlinePad)
  print a.node_list
  a.getArticles()

def get_article_htmls():
  print "get article html"
  a = ArticleHtmlProc()
  a.createContentPage()
  a.createListPage()
  return
