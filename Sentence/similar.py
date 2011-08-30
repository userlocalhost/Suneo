#!/usr/bin/python
#-*- coding: utf-8 -*-

#
# Date      : 2011/08/24
# Author    : Hiroyasu OHYAMA 
# Belonged  : Ariel-Network Inc. (http://www.ariel-networks.com)
#           : Ariel Lab (http://)
# 
# copyright(c) 2011 Hiroyasu OHYAMA. all-right reserved.
#

from xml.etree.ElementTree import ElementTree
from urllib import urlopen, unquote
from subprocess import Popen, PIPE
import sys
import os
import re

def _forming_for_weblio(path):
	xmllist = []
	result_path = ".tmp_output"
	f = open(path, 'r')
	
	addList = False

	# append start point
	xmllist.append("<root>")

	while True:
		line = f.readline()
		if not line:
			break
	
		line = line[:-1]
		line = unquote(line)
		line = re.sub('class=([a-zA-Z0-9]+)', 'class="\\1"', line)
		line = re.sub(' ・ ', '\n', line)
	
		if re.compile('<table>').match(line):
			addList = True
	
		if addList:
			xmllist.append(line)
	
		if re.compile('</table>').match(line):
			addList = False
	
	# append end point
	xmllist.append("</root>")
	
	f.close()

	# write result into result file
	f = open(result_path, 'w')
	for line in xmllist:
		f.writelines(line)

	f.close()

	return result_path

def _get_similar_wordset(path):
	wordset = set([]);
	xml = ElementTree(file=open(path))
	root = xml.getroot()
	
	elements = root.findall('.//a');
	wordset = set([])
	for elem in elements:
		wordset.add(elem.text)
	
	return wordset

def _get_similar_xml(word):
	url = "http://thesaurus.weblio.jp/content/" + word
	result_path = ".test.html"

	os.system("wget -O %s %s &> /dev/null" % (result_path, url))

	return result_path

def _breakdown_into_validwords(str):
	ret_list = []
	f = open('input.txt', 'w')
	f.write(str.encode('utf-8'))
	f.close()
	
	p = Popen(["mecab", "input.txt"], stdout=PIPE)
	while 1:
		line = p.stdout.readline()[:-1]
		if not line:
			break
	
		result = re.compile("^.*\s+(.*)$").findall(line)
		if result:
			result = result[0].split(',')
			type = result[0]
			value = result[6]
		
			#if (type == '名詞' or type == '動詞' or type == '形容詞') and value != '*':
			if (type == '名詞') and value != '*':
				#print "type:%s, value:%s" % (type, value)
				ret_list.append(value)
	
	p.wait()

	return ret_list

def concat(src, dst=[]):
	for item in src:
		if type(item).__name__ == 'list':
			concat(item,dst)
		else:
			dst.append(item)
	return dst

class SimilarWord:
	
	def __init__(self, word):
		self.word = word
	
	def get(self):
		xmlpath = _get_similar_xml(self.word)
		
		# forming getting xml file
		xmlpath = _forming_for_weblio(xmlpath)
		
		# get wordset of similar word
		wordset = _get_similar_wordset(xmlpath)
		
		return list(set(concat(map((lambda x: _breakdown_into_validwords(x)), wordset))))
