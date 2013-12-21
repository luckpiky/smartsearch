# coding=gb2312

import re,string
import time

LINE_ANY_STR = "__LINE_ANY_STR"
ANY_NUM_LINE = "__ANY_NUM_LINE-"

RULE_KEY_INCLUDE = "include"
RULE_KEY_INCLUDEOR = "include-or"
RULE_KEY_EQUAL = "equal"
RULE_KEY_PATTERN = "pattern"

ANY_NUM_LINE_FLAG = 1

class SmartScript():
	rules = []
	result = []
	def __init__(self):
		self.rules = []
		self.result = []
		self.matched_line_format = 1 #0表示以文本形式返回，1表示以列表形式返回
		self.obj = None
		self.do_equal = 0
		self.do_pattern = 0
		return

	#添加规则行
	def add_rule_line(self, rule):
		self.rules.append(rule.strip())
		return 

	def clear_rule(self):
		del self.rules[0:len(self.rules)]
		return

	#检查参数s是否是一个数字
	def is_integer(self, s):
		c = r'\d+'
		d = re.match(c, s)
		if None == d:
			return False, s
		c = r'\D+'
		if None != re.search(c, s):
			return False, s
		return True, string.atoi(s)


	#正则表达式匹配
	def pattern_line_match(self, rule, line, values):
		if None == rule or None == line:
			return False

		rule_pattern = re.compile(rule)
		if None == rule_pattern:
			return False
		matched = re.match(rule_pattern, line)
		if None == matched:
			return False
		if None == values:#如果values为空，表示只比较不取数据
			return True
		keys = []
		self.get_key(keys, rule)
		for k in keys:
			a1,a2 = self.is_integer(matched.group(k))
			values[k] = a2
		return True

	#比较一行是否匹配，支持equal和pattern		
	def is_match(self, line, rule, type, values):
		if LINE_ANY_STR == rule:
			return True
		if RULE_KEY_EQUAL == type and line == rule:
			self.do_equal = self.do_equal + 1
			return True
		if RULE_KEY_PATTERN == type and self.pattern_line_match(rule, line, values):
			self.do_pattern = self.do_pattern + 1
			return True
		return False


	#从规则中取出关键字
	def get_key(self, value_list, pattern_str):
		f1 = ''
		f2 = 0
		f3 = 0
		for i in range(0, len(pattern_str)):
			if pattern_str[i] == '(':
				f1 = '('
				f2 = i
				continue
			if f2 == i - 1:
				if ('(' == f1) and ('?' == pattern_str[i]):
					f1 = '?'
					f2 = i
				elif ('?' == f1) and ('P' == pattern_str[i]):
					f1 = 'P'
					f2 = i
				elif ('P' == f1) and ('<' == pattern_str[i]):
					f3 = i + 1
			elif f3 != 0:
				if '>' == pattern_str[i]:
					value_list.append(pattern_str[f3:i])
					f3 = 0
			else:
				f3 = 0
				f1 = ''
				f2 = 0
		return

	#多行匹配
	def do_match(self, contents, match_type):
		rule_tmp = self.rules					
		lines_tmp = []
		match_first_rule = False
		rule_key_tmp = []
	
		#对规则进行预处理
		for r in rule_tmp:
			if -1 !=  r.find(ANY_NUM_LINE):
				t = r.split("-")
				if len(t) >= 2:
					t2 = [ANY_NUM_LINE_FLAG, string.atoi(t[1])]
					rule_key_tmp.append(t2)
			else:
				rule_key_tmp.append([0,0])

		for line in contents:	
			line = line.strip()
			
			#进行首规则匹配，以增加匹配速度
			if False == match_first_rule:
				if False == self.is_match(line, rule_tmp[0], match_type, None):
					continue
				else:
					match_first_rule = True

			lines_tmp.append(line)
			any_num_line = 0
			next_match_rule_line = 0 
			if len(lines_tmp) >= len(rule_tmp):
				c = 0
				j = 0
				matched = False

				arg_item = {"matched_line":[], "values":{}}

				#开始匹配
				for i in range(0,len(lines_tmp)): 
					#先做ANY_NUM_LINE匹配，如果rule为ANY_NUM_LINE，则获取最大跳过的行数，
					#直接匹配下一个rule行，如果匹配成功则跳到下下个rule行比较	
					if 0 == any_num_line and ANY_NUM_LINE_FLAG == rule_key_tmp[j][0]:
						#t = rule_tmp[j].split("-")
						#if len(t) >= 2:
						any_num_line = rule_key_tmp[j][1] + 2  #获取最大跳过行数
						next_match_rule_line = j + 1  #下一个rule行的下标
						if next_match_rule_line >= len(rule_tmp):
							next_match_rule_line = 0
					if any_num_line > 0: #控制跳过行数
						any_num_line = any_num_line - 1

					if 0 != any_num_line and 0 != next_match_rule_line: #条件满足的情况下进行下一个rule行匹配
						if True == self.is_match(lines_tmp[i], rule_tmp[next_match_rule_line], match_type, arg_item["values"]):
							j = j + 2
							next_match_rule_line = 0
							any_num_line = 0
							if j == len(rule_tmp): #命中最后一个rule行，则认为完全匹配成功
								matched = True
								break
							#下一个rule行匹配匹配成功，则清空ANY_NUM_LINE
						continue

					#非ANY_NUM_LINE比较，这个是逐行比较，必须每行都一致			
					if False == self.is_match(lines_tmp[i], rule_tmp[j], match_type, arg_item["values"]):
						lines_tmp.pop(0)
						c = -1
						break
					else:
						if j == len(rule_tmp) - 1:
							matched = True
							break
						j = j + 1 #匹配成功一个，rule就向后移动一个
					c = c + 1
		
				if matched: #匹配成功
					m = 0
					for tmp in lines_tmp:
						arg_item["matched_line"].append(tmp)
						if None != self.obj:
							if 0 == m:
								self.obj.info = tmp
							else:
								self.obj.info = self.obj.info + "\n" + tmp
							m = m + 1
					self.result.append(arg_item)
					del lines_tmp[0:len(lines_tmp)] #清空lines_tmp

		return

	def pattern_match(self, lines):
		self.do_match(lines,RULE_KEY_PATTERN)
		return

	def equal_match(self, lines):
		self.do_match(lines, RULE_KEY_EQUAL)
		return

	def match_key_line(self, lines, key):
		matched_lines = []
		for line in lines:
			if -1 != line.find(key):
				matched_lines.append(line)
		return matched_lines

	def cut_range_lines(self, lines, flag):
		step = 0
		c = 0
		info = ""
		start = 0
		end = 0
		arg_item = {"matched_line":[], "values":{}}

		#先预查找一次，以避免存取速度太慢或太费内存
		for line in lines:
			line = line.strip()
			if 0 == step and self.rules[0] == line:
				step = 1
				start = c
			elif 1 == step and self.rules[1] == line:
				step = -1
				end = c + 1
				break
			c = c + 1

		if -1 != step:
			return False

		#找到后，直接获取
		self.info = ""
		for i in range(start, end):
			arg_item["matched_line"].append(lines[i])
			if None != self.obj:
				if start == i:
					self.obj.info = lines[i].strip()
				else:
					self.obj.info = self.obj.info + "\n" + lines[i].strip()
		self.result.append(arg_item)
		return True
				
