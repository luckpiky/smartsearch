# coding=utf-8

#!/usr/bin/env python
import os
import sys
import spider

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    print sys.argv
    if 3 == len(sys.argv):
        # 获取文章
        if 'article' == sys.argv[2]:
           from spider.articles import *
           get_articles()
        # 生成页面
        if 'article_htmls' == sys.argv[2]:
           from spider.articles import *
           get_article_htmls()
    else:
        execute_from_command_line(sys.argv)
    
   


            
