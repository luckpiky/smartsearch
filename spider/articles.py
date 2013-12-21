# coding=utf-8 #

import urllib
import string
import os
import time
from spider.models import *
from spider.article.zol_pad import *
from spider.article.pconline_pad import *
from spider.article.cnmo_pad import *
from django.core.paginator import *
from django.template.loader import get_template
from django.template import Context
from config.settings import *

from spider.product.zol_pad_list import *

reload(sys)
sys.setdefaultencoding('utf-8')


#article processor
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
   
    typeid = self.getTypeIdByIname(node.atype)
    if -1 != typeid:
      article.type_id = typeid

    article.title = title.encode('utf-8')
    article.url = url
    article.content = content 
    article.site = node.site
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
    tmp_url = node.url
    print tmp_url
    while(None != tmp_url):
      #print node.page
      article_list = node.getArticleList(tmp_url)
      print 'read ' + str(len(article_list)) + ' articles'

      #get next list page
      tmp = node.getNextListPage(tmp_url)
      if None != tmp:
        tmp_url = urljoin(url, tmp)
        print tmp_url
        page_index = page_index + 1
      else:
        tmp_url = None

      # read aritcle content
      for article in article_list:
        print article[0],article[1] # title url
        
        #control the count
        count = count + 1
        if count > self.MAX_READ_PERNODE:
            return

        # check and read and write a article
        if self.checkArticleExist(article[0], article[1]):
          content = node.getArticleContent(article[1])

          # write to file
          if None != content and '' != content:
            self.writeArticle(article[0], article[1], content, node)      
          continue
    return

  def getArticles(self):
    for node in self.node_list:
      print 'get ',node[0],node[1].url
      self.getArticle(node[1])
    return

  def renewArticles(self):
    articles = SmtArticle.objects.all()
    for a in articles:
      for tnode in self.node_list:
        tnode = tnode[1]
        if tnode.site == a.site:
          content = tnode.getArticleContent(a.url)
          a.content = content
          a.description = getContentDescription(content, self.MAX_DESCRIPTION)
          a.save()
    return

  def register(self, name, node):
    has = False
    for t in self.node_list:
      if t[0] == name:
        has = True
        break
    if False == has:
      print 'regiter:',name,node
      self.node_list.append([name, node])
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
      html = t.render(Context({'articles':articles, 'pages':pages, 'first_page':first_page, 'pre_page':pre_page, 'next_page':next_page, 'last_page':last_page, 'list_type':list_type}))
      self.writeFile(filename, html)

    return

  def createContentPage(self):
    rst = SmtArticle.objects.filter(status=True).all()
    for item in rst:
      filename = STATIC_ROOT + 'article_' + str(item.id) + '.html'

      if False == self.canWrite(filename):
        continue

      #format content
      item.content = removeScript(item.content)
      item.content = removeUrls(item.content)
      item.content = formatImg(item.content)

      t = get_template('article.html')
      html = t.render(Context({'article':item}))
      self.writeFile(filename, html)
    return 



def createArticleNode():
  a = Article()
  zol_pad = ArticleZolPad()
  zol_pad.setBaseUrl("http://pad.zol.com.cn/more/2_1531.shtml")
  a.register('zolpad_article', zol_pad)
  
  pconline_pad = ArticlePconlinePad()
  pconline_pad.setBaseUrl("http://pad.pconline.com.cn/reviews/");
  a.register('pconlinepad_article', pconline_pad)

  cnmo_pad = ArticleCnmoPad()
  cnmo_pad.setBaseUrl("http://pad.cnmo.com/list_50_52_0_1.html");
  a.register('cnmopad_article', cnmo_pad)

  return a

def get_articles():
  print "get articles"
  a = createArticleNode()
  a.getArticles()
  return

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

def renew_articles():
  a = createArticleNode()
  a.renewArticles() 


def createProductParseNode():
  #a = Article()
  #zol_pad = ArticleZolPad()
  #zol_pad.setBaseUrl("http://detail.zol.com.cn/tablepc/")
  #a.register('zolpad_product', zol_pad)
  
  return a


def get_product_list():
  node = ProductZolPad()
  node.setBaseUrl("http://detail.zol.com.cn/tablepc/")

  tmp_url = node.url
  while(tmp_url):
    lst = node.getArticleList(tmp_url)
    for item in lst:
      print item[0],item[1]
      page_url = urljoin(node.url, item[1])
      node.getArticleContent(item[0] , page_url)
    
    #get next list page
    tmp = node.getNextListPage(tmp_url)
    if None != tmp:
      tmp_url = urljoin(node.url, tmp)
      print 'next page:',tmp_url
    else:
      tmp_url = None


  return

