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
		self.matched_line_format = 1 #0��ʾ���ı���ʽ���أ�1��ʾ���б���ʽ����
		self.obj = None
		self.do_equal = 0
		self.do_pattern = 0
		return

	#��ӹ�����
	def add_rule_line(self, rule):
		self.rules.append(rule.strip())
		return 

	def clear_rule(self):
		del self.rules[0:len(self.rules)]
		return

	#������s�Ƿ���һ������
	def is_integer(self, s):
		c = r'\d+'
		d = re.match(c, s)
		if None == d:
			return False, s
		c = r'\D+'
		if None != re.search(c, s):
			return False, s
		return True, string.atoi(s)


	#������ʽƥ��
	def pattern_line_match(self, rule, line, values):
		if None == rule or None == line:
			return False

		rule_pattern = re.compile(rule)
		if None == rule_pattern:
			return False
		matched = re.match(rule_pattern, line)
		if None == matched:
			return False
		if None == values:#���valuesΪ�գ���ʾֻ�Ƚϲ�ȡ����
			return True
		keys = []
		self.get_key(keys, rule)
		for k in keys:
			a1,a2 = self.is_integer(matched.group(k))
			values[k] = a2
		return True

	#�Ƚ�һ���Ƿ�ƥ�䣬֧��equal��pattern		
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


	#�ӹ�����ȡ���ؼ���
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

	#����ƥ��
	def do_match(self, contents, match_type):
		rule_tmp = self.rules					
		lines_tmp = []
		match_first_rule = False
		rule_key_tmp = []
	
		#�Թ������Ԥ����
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
			
			#�����׹���ƥ�䣬������ƥ���ٶ�
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

				#��ʼƥ��
				for i in range(0,len(lines_tmp)): 
					#����ANY_NUM_LINEƥ�䣬���ruleΪANY_NUM_LINE�����ȡ���������������
					#ֱ��ƥ����һ��rule�У����ƥ��ɹ����������¸�rule�бȽ�	
					if 0 == any_num_line and ANY_NUM_LINE_FLAG == rule_key_tmp[j][0]:
						#t = rule_tmp[j].split("-")
						#if len(t) >= 2:
						any_num_line = rule_key_tmp[j][1] + 2  #��ȡ�����������
						next_match_rule_line = j + 1  #��һ��rule�е��±�
						if next_match_rule_line >= len(rule_tmp):
							next_match_rule_line = 0
					if any_num_line > 0: #������������
						any_num_line = any_num_line - 1

					if 0 != any_num_line and 0 != next_match_rule_line: #�������������½�����һ��rule��ƥ��
						if True == self.is_match(lines_tmp[i], rule_tmp[next_match_rule_line], match_type, arg_item["values"]):
							j = j + 2
							next_match_rule_line = 0
							any_num_line = 0
							if j == len(rule_tmp): #�������һ��rule�У�����Ϊ��ȫƥ��ɹ�
								matched = True
								break
							#��һ��rule��ƥ��ƥ��ɹ��������ANY_NUM_LINE
						continue

					#��ANY_NUM_LINE�Ƚϣ���������бȽϣ�����ÿ�ж�һ��			
					if False == self.is_match(lines_tmp[i], rule_tmp[j], match_type, arg_item["values"]):
						lines_tmp.pop(0)
						c = -1
						break
					else:
						if j == len(rule_tmp) - 1:
							matched = True
							break
						j = j + 1 #ƥ��ɹ�һ����rule������ƶ�һ��
					c = c + 1
		
				if matched: #ƥ��ɹ�
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
					del lines_tmp[0:len(lines_tmp)] #���lines_tmp

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

		#��Ԥ����һ�Σ��Ա����ȡ�ٶ�̫����̫���ڴ�
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

		#�ҵ���ֱ�ӻ�ȡ
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
				
