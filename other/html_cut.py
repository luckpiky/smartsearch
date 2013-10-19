import re
import urllib
import string
from HTMLParser2 import *
from urlparse import *
from HtmlParserEngine import *

get_tags = ['img','a','br','p']

def check_get_tag(tag):
    for t in get_tags:
        if tag == t:
            return True
    return False

class HtmlCut(HTMLParser):
    def __init__(self, rule):
        self.rule = rule
        self.init_item = None
        self.at = 0
        self.data = []
        self.item = []
        self.tmp = None
        self.last_tag = ''
        self.cut = False
        self.stack = []
        self.tag = ''
        self.cutstr = ''
        HTMLParser.__init__(self)
        return
    
    def set_initfunc(self, func):
        self.init_item = func
        self.item = self.init_item()
        return
    
    def get_value(self, para1, para2, value):
        value = value.strip()
        if 0 == len(value):
            return
        if 'all' == para2:
            self.item[para1] = self.item[para1] + value
        elif 'last' == para2:
            self.item[para1] = value
        elif 'first' == para2:
            if '' == self.item[para1]:
                self.item[para1] = value
        else:
            self.item[para1] = value
        return
    
    def cut_content(self, flag, arg1, arg2):
        if False == self.cut:
            return False
        cut_str = ''
        start_cut_tag = ''
        if len(self.stack) == 0:
            start_cut_tag = arg1
        else:
            start_cut_tag = self.stack[0]
        if 'start' == flag:
            if None != arg1 and check_get_tag(arg1):
                cut_str = '<'+arg1
                if None != arg2:
                    for name,value in arg2:
                        cut_str = cut_str + ' ' + name + '="' + value + '"'
                cut_str = cut_str + '>'
            if arg1 == start_cut_tag:
                self.stack.append(arg1)
        if 'data' == flag:
            cut_str = arg1
        if 'end' == flag:
            if check_get_tag(arg1):
                cut_str = '</' + arg1 + '>'
            if arg1 == start_cut_tag:
                self.stack.pop()
                if 0 == len(self.stack):
                    self.cut = False
        self.cutstr = self.cutstr + cut_str
        return True
    
    def check_tag(self):
        if self.at >= len(self.rule):
            return
        debug_check(self.rule[self.at])
        rule = self.rule[self.at]
        if 'goto' == rule[0]:
            self.at = rule[1]
            return
        if 'cut' == rule[0]:
            self.cut = True
            self.at = self.at + 1
            return
        if 'getitem' == rule[0]:
            self.item['#cut'] = self.cutstr
            self.cutstr = ''
            self.data.append(self.item)
            self.item = self.init_item()
            self.at = self.at + 1
            return
        if 'ignore' == rule[0]:
            self.at = self.at + 1
            return
        return
    
    def check_attrs(self, attrs1, attrs2):
        checked_count = 0
        for name,value in attrs1:
            for tmp in attrs2:
                if tmp[0] == name:
                    if '#' == tmp[1][0]:
                        self.get_value(tmp[1], tmp[2], value)
                        checked_count = checked_count + 1
                    elif tmp[1] == value:
                        checked_count = checked_count + 1
        if checked_count == len(attrs2):
            return True
        return False
    
    def handle_starttag(self, tag, attrs):
        debug_found('start '+tag)
        self.tag = tag
        if self.cut_content('start', tag, attrs):
            return
        self.check_tag()
        if self.at >= len(self.rule):
            return
        rule = self.rule[self.at]
        if 'start' != rule[0] or tag != rule[1]:
            return
        attr = rule[2]
        if self.check_attrs(attrs, attr):
            self.tmp = None
            self.at = self.at + 1
            self.check_tag()     
        self.last_tag = tag
        return

    def handle_data(self, data):
        debug_found('data '+data)
        if self.cut_content('data', data, None):
            return        
        self.check_tag()
        if self.at >= len(self.rule):
            return
        rule = self.rule[self.at]
        if 'data' != rule[0] and None == self.tmp:
            return
        
        if 'data' == rule[0]:
            self.at = self.at + 1
            if '' != rule[2] and None == self.tmp:
                self.tmp = rule
        else:
            rule = self.tmp
            
        self.get_value(rule[1], rule[2], data)
        
        self.check_tag()
        return
    
    def handle_endtag(self, tag):
        debug_found('end '+tag)
        if self.cut_content('end', tag, None):
            return        
        self.check_tag()
        if self.at >= len(self.rule):
            return
        rule = self.rule[self.at]
        if 'end' != rule[0]:
            return
        if rule[1] == tag:
            self.tmp = None
            self.at = self.at + 1
            self.check_tag()    
        return
