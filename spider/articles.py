# coding=utf-8 #

import urllib
import string
import os
import time
from spider.models import *
from spider.article.zol_pad import *
from spider.article.pconline_pad import *
from django.core.paginator import *
from django.template.loader import get_template
from django.template import Context
from config.settings import *

reload(sys)
sys.setdefaultencoding('utf-8')

class Article():
  def __init__(self):
    self.node_list = []
    self.MAX_READ_PERNODE = 20
    self.MAX_DESCRIPTION = 100
    return

  def getTypeIdByIname(self, iname):
    types = SmtArticleType.objects.filter(iname=iname).all()
    if None == types or len(types) == 0:
      return -1
    return types[0].id

  def writeArticle(self, title, url, content, node):
    article = SmtArticle()
   
    typeid = self.getTypeIdByIname(node.iname)
    if -1 != typeid:
      article.type_id = typeid

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
    self.rewrite = False
    return

  def canWrite(self, filename):
    if True == self.rewrite:
      return True
    if False == os.path.exists(filename):
      return True
    return False

  def writeFile(self, filename, content):
    fp = open(filename, 'w')
    fp.write(content)
    fp.close()
    print 'create', filename, 'ok'
    return

  def createListPage(self, list_type):
    c = 0
    page_count = 0
    page = 1
    rst = None
    file_name_pre = ""

    if 'all' == list_type:
      rst = SmtArticle.objects.filter(status=True).order_by("-id").all()
      file_name_pre = 'article_list_'
    else:
      t = Article()
      typeid = t.getTypeIdByIname(list_type)
      rst = SmtArticle.objects.filter(type=typeid).filter(status=True).order_by("-id").all()
      file_name_pre = 'article_list_' + list_type + '_'
    if None == rst or len(rst) == 0:
      return
    page_count = len(rst) / self.COUNT_PER_PAGE
    if len(rst) % self.COUNT_PER_PAGE > 0:
      page_count = page_count + 1
    print 'total page:',page_count

    pages = []
    for page in range(1, page_count + 1):
      pages.append(page)
    for page in range(1, page_count + 1):
      paginator = Paginator(rst, self.COUNT_PER_PAGE)
      articles = paginator.page(page)
      first_page = 1
      last_page = page_count
      pre_page = page - 1
      if pre_page == 0:
        pre_page = 1
      next_page = page + 1
      if next_page > page_count:
        next_page = page_count
      
      #now begin create article_list_X.html
      filename = STATIC_ROOT + file_name_pre + str(page) + '.html'
      
      t = get_template('articles_list.html')
      html = t.render(Context({'articles':articles, 'pages':pages, 'first_page':first_page, 'pre_page':pre_page, 'next_page':next_page, 'last_page':last_page}))
      
      self.writeFile(filename, html)

    return

  def createContentPage(self):
    rst = SmtArticle.objects.filter(status=True).all()
    for item in rst:
      filename = STATIC_ROOT + 'article_' + str(item.id) + '.html'

      if False == self.canWrite(filename):
        continue

      t = get_template('article.html')
      html = t.render(Context({'article':item}))
      self.writeFile(filename, html)
    return


def get_articles():
  print "get articles"
  a = Article()
  a.register('zolpad', ArticleZolPad)
  a.register('pconlinepad', ArticlePconlinePad)
  print a.node_list
  a.getArticles()

def get_article_htmls(operation):
  print "get article html"
  a = ArticleHtmlProc()
  if 'all' == operation:
    a.rewrite = True
  a.createContentPage()
  a.createListPage('all')
  rst = SmtArticleType.objects.all()
  for t in rst:
    a.createListPage(t.iname)
  return
