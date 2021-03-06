# coding=utf-8


import re
import urllib
import string
from HTMLParser2 import *
from urlparse import *

################################################################
#全局变量以及符号
################################################################

#预定义的html标签
PRE_TAGS = ['img','a','br','p']

#规则检查的debug开关
DEBUG_FLAG_ENGINE_CHECK = False

#找到操作的debug开关
DEBUG_FLAG_ENGINE_FOUND = False


################################################################
#工具函数
################################################################

#获取page的绝对路径
def get_abspath(url, page):
    return urljoin(url, page)


#检查某个标签是否是预定义的标签
def check_get_tag(tag):
    for t in PRE_TAGS:
        if tag == t:
            return True
    return False


#规则匹配debug
def debug_check(rule):
    if False == DEBUG_FLAG_ENGINE_CHECK:
        return
    print 'to find:',rule
    print
    
#查到后的debug
def debug_found(str):
    if False == DEBUG_FLAG_ENGINE_FOUND:
        return
    print 'found:',str
    print


################################################################
#规则编译类
################################################################
class HtmlParserCompiler(HTMLParser):
    def __init__(self):
        self.rule = []
        HTMLParser.__init__(self)
        return

    #从文本中获取值
    def get_value(self, value):
        if '#' != value[0]:
            return value,''
        tmp = value.split('-')
        if 2 == len(tmp):
            return tmp
        else:
            return tmp[0],''

    #起始标签处理
    #支持的语句为:
    #goto
    #getitem
    #cut    
    def handle_starttag(self, tag, attrs):
        tag = tag.strip()
        item = []
        tmp = tag.split('-')
        if 'goto' == tmp[0]:
            item.append('goto')
            item.append(string.atoi(tmp[1]))
            self.rule.append(item)
            return
        if 'getitem' == tmp[0]:
            item.append('getitem')
            self.rule.append(item)
            return
        if 'cut' == tmp[0]:
            item.append('cut')
            self.rule.append(item)
            return            
        
        item = ['start']
        item.append(tag)
        attr = []
        for name,value in attrs:
            v1,v2 = self.get_value(value)
            tmp2 = [name, v1,v2]
            attr.append(tmp2)
        item.append(attr)
        self.rule.append(item)
        return
    
    #数据字段处理
    def handle_data(self, data):
        data = data.strip()
        if 0 == len(data):
            return
        v1,v2 = self.get_value(data)
        item = ['data', v1, v2]
        self.rule.append(item)
        return

    #结束标签处理
    def handle_endtag(self, tag):
        item = ['end', tag]
        self.rule.append(item)
        return


#################################################################
#规则匹配类
################################################################
class HtmlParserMatch(HTMLParser):
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
    
    #注册回调函数
    def set_initfunc(self, func):
        self.init_item = func
        self.item = self.init_item()
        return
    
    #取值，支持一下方法：
    #all
    #last
    #first
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
    
    #从页面中截取一段内容
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
    
    #标签检查
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
    
    #检查属性
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
    
    #起始标签
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

    #数据
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
    
    #结束标签
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


class HtmlParserMatch2(HTMLParser):
    def __init__(self, rule):
        self.rule = rule
        self.init_item = None
        self.at = 0
        self.data = []
        self.item = []
        self.tmp = None
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
    
    def check_tag(self):
        if self.at >= len(self.rule):
            return
        debug_check(self.rule[self.at])
        rule = self.rule[self.at]
        if 'goto' == rule[0]:
            self.at = rule[1]
            return
        if 'getitem' == rule[0]:
            self.data.append(self.item)
            self.item = self.init_item()
            self.at = self.at + 1
            return
        if 'ignore' == rule[0]:
            self.at = self.at + 1
            return
        return
    
    def handle_starttag(self, tag, attrs):
        debug_found('start '+tag)
        self.check_tag()
        if self.at >= len(self.rule):
            return
        rule = self.rule[self.at]
        if 'start' != rule[0] or tag != rule[1]:
            return
        attr = rule[2]
        checked_count = 0
        for name,value in attrs:
            for tmp in attr:
                if tmp[0] == name:
                    if '#' == tmp[1][0]:
                        self.get_value(tmp[1], tmp[2], value)
                        checked_count = checked_count + 1
                    elif tmp[1] == value:
                        checked_count = checked_count + 1
        if checked_count == len(attr):
            self.tmp = None
            self.at = self.at + 1
            self.check_tag()
        return

    def handle_data(self, data):
        debug_found('data '+data)
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

class PageFormat(HTMLParser):
    def __init__(self):
	self.page = ''
        self.url = ''
        return

    def set_mainurl(self, url):
        self.url = url
        return

    def handle_starttag(self, tag, attrs):
        self.page = self.page + ' <' + tag
	for n,v in attrs:
            if n == 'src':
                v = get_abspath(self.url, v)
            self.page = self.page + ' ' + n + '="' + v + '"'
	self.page = self.page + '>\n'
        return

    def handle_data(self, data):
        self.page = self.page + data + '\n'
        return

    def handle_endtag(self, tag):
        self.page = self.page + ' </' + tag + '>\n'
        return





