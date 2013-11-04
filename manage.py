# coding=utf-8

#!/usr/bin/env python
import os
import sys
import spider

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    print sys.argv
    #if 3 == len(sys.argv):
    # get article html page content and store to database
    if 'get_article' == sys.argv[1]:
      from spider.articles import *
      get_articles()
    # create new html page
    elif 'create_html_new' == sys.argv[1]:
      from spider.articles import *
      get_article_htmls('new')
    elif 'create_html_all' == sys.argv[1]:
      from spider.articles import *
      get_article_htmls('all')
    elif 'renew_article' == sys.argv[1]:
      from spider.articles import *
      renew_articles()
      print 'aa'
    else:
      execute_from_command_line(sys.argv)
    
   


            
