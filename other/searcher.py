import re
import urllib
import string
import os
from urlparse import *
from HtmlParserEngine import *
from html_cut import *
import time

TYPE_URL = 1
TYPE_PAGE = 2

def echo_str(str):
    if str != '':
        print str
    return

class search_1:
    def __init__(self):
        self.rule = ''
        self.type = 0
        return
    
    def set_type(self, type):
        self.type = type;
        return
    
    def init_item(self):
        return {'#url':'', '#title':'', '#replycount':'', '#time':'', '#readcount':'', '#cut':''}    
    
    def compiler(self, rule, code):
        if '' != code:
            compiler_file = open(rule).read().decode(code)
        else:
            compiler_file = open(rule).read()
        compiler = HtmlParserComplier()
        compiler.feed(compiler_file)
        self.rule = compiler.rule  
        return    
    
    def parser(self, url, code):
        page = urllib.urlopen(url).read().decode(code)
        urlmatcher = HtmlParserMatch(self.rule)
        urlmatcher.set_initfunc(self.init_item)
        urlmatcher.feed(page)
        return urlmatcher.data
        
    def search(self, rule, code1, code2, url):
        self.compiler(rule, code1)
        data = self.parser(url, code2)
        self.print_data(data, self.type)
        return
    
    def print_data(self, data, type):
        for t in data:
            if type == TYPE_PAGE:
                echo_str(t['#cut'])
                print
            else:
                replycount = 0
                if t['#replycount'] != '':
                    replycount = string.atoi(t['#replycount'])
                if replycount < 50:
                    continue
                echo_str(t['#title'])
                echo_str(t['#url'])
                echo_str(t['#replycount'])
                echo_str(t['#readcount'])
                echo_str(t['#time'])
                print
        return
    
