# coding=utf-8 #


import urllib
import string
import os
import time

from BeautifulSoup import * 

#将文本中的url全改为绝对路径
def formatUrl(content, url):
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
def removeUrls(content):
    #content = content.decode('gbk')
    soup = BeautifulSoup(content)
    tmp1 = soup.findAll('a')
    for tmp2 in tmp1:
        a = tmp2.__str__()
        b = tmp2.contents
        if None != b and len(b) > 0:
            content = content.replace(a, str(b[0]))
    return content
    [tmp2.extract() for tmp2 in tmp1]
    return soup.renderContents()

def removeScript(content):
  soup = BeautifulSoup(content)
  t = soup.findAll('script')
  [a.extract() for a in t]
  t = soup.findAll('noscript')
  [a.extract() for a in t]
  return str(soup)
  

img_exts = ['jpg', 'png', 'bmp', 'gif', 'jpeg']


#去除img标签中的多余信息，只留下src,height,width
def formatImg(content):
    soup = BeautifulSoup(content)
    tmp1 = soup.findAll('img')
    true_pic = False
    for tmp in tmp1:
        new_img = '<img src ="' + tmp['src'] + '"'
        #try:
        #    if None != tmp['height']:
        #        new_img = new_img + ' height="' + tmp['height'] + '"'
        #except:
        #    pass
        #try:
        #    if None != tmp['width']:
        #        new_img = new_img + ' width="' + tmp['width'] + '"'
        #except:
        #    pass
        for t in img_exts:
          if -1 != tmp['src'].lower().find(t):
            true_pic = True
        if true_pic:
          new_img = new_img + ' border="0" class="main_pic"'
        new_img = new_img + ' />'
        content = content.replace(tmp.__str__(), new_img)
    return content

#获取文本中的所有P节点
def getPNode(page):
    content = ''
    soup = BeautifulSoup(page)
    ps = soup.findAll('p')
    if None != ps:
        for t in ps:
            content = content + '\n' + str(t)
    return content

def delPreStr(s, c):
  len_c = len(c)
  if len(s) > len_c:
    if s[0:len_c] == c:
      return delPreStr(s[len_c:(len(s) - len_c)], c)
    else:
      return s
  return s


def getContentDescription(content, count):
    soup = BeautifulSoup(content)
    t = soup.contents[0].string
    s = ''
    while None != t:
      if None != t.string:
        s = s + t.string
        if len(s) > count * 2:
          break
      t = t.next
    s1 = delPreStr(s, '\r\n')
    s2 = delPreStr(s1, '\n')
    s1 = delPreStr(s2, ' ')
    s2 = delPreStr(s1, '&nbsp;')
    if len(s2) > count:
      return s2[0:count]
    return s2

def getFirstPicture(content):
  soup = BeautifulSoup(content)
  t = soup.findAll('img')
  first_pic = ""
  if None != t:
    for a in t:
      if None == a['src']:
        continue
      if "" == first_pic:
        first_pic = a['src']
      for t in img_exts:
        if -1 != a['src'].lower().find(t):
          print 'find',a['src']
          return a['src']
      print 'find first'
  return first_pic


