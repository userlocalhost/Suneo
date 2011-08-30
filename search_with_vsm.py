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

from subprocess import Popen, PIPE
from os import system

# These are original component
from Sentence.sentence import *
from Sentence.similar import *
from Sentence.word import *

import re
import sys
import argparse
import os.path

def breakdown_into_validwords(str):
	ret_list = []
	f = open('.input.txt', 'w')
	f.write(str)
	f.close()
	
	p = Popen(["mecab", ".input.txt"], stdout=PIPE)
	while 1:
		line = p.stdout.readline()[:-1]
		if not line:
			break
	
		result = re.compile("^.*\s+(.*)$").findall(line)
		if result:
			result = result[0].split(',')
			type = result[0]
			value = result[6]
		
			if (type == '名詞' or type == '動詞' or type == '形容詞') and value != '*':
				#print "type:%s, value:%s" % (type, value)
				ret_list.append(value)
	
	p.wait()

	return ret_list

#
# Init processing of constructing Sentence objects and Validwords objects
# 
# Following is the sequence of this script.
#
# 2. break down it onto list of words.
# 3. create Sentence object.
# 4. create, init and regist Validword object
# 5. init and regist Sentence object.
#
def init_evaluation_environment(string, relate_similar_words=False):
	sentence_obj = None
		
	# 2. break down it onto list of words.
	if relate_similar_words:
		word_list = concat(map((lambda x:SimilarWord(x).get()), breakdown_into_validwords(string)))
	else:
		word_list = breakdown_into_validwords(string)

	# This condition assures there are valid-words in this sentence at least one.
	if word_list != []:
	
		# 3. create Sentence object.
		sentence_obj = Sentence(string)

		#for word in word_list:
		for word in word_list:
			valid_obj = Validword.get_wordobj(word)
			if valid_obj == None:
				# create new Validword object and regist it
				valid_obj = Validword(word)
				Validword.append_validword(word, valid_obj)

			# regist sentence-id to Validword object
			valid_obj.add_sentence_id(sentence_obj.get_id())

			# init Sentence object
			sentence_obj.regist_word(word)
	
	return sentence_obj

def eval_similarity(sentence):
	related_sentence_list = set([])

	for word in sentence.get_wordlist():
		sentence_list = word.get_sentences()

		for sentence_id in sentence_list:
			sentence_obj = Sentence.getobj_from_id(sentence_id)

			if sentence_obj != None:
				related_sentence_list.add(sentence_obj)

	for item in related_sentence_list:
		similar_degree = sentence.similar_degree(item)
		if similar_degree > 0:
			print "[eval_similarity] %s : %f" % (item.get_content(), similar_degree)

def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-s', action='store', dest='sentence_path', 
			help = 'Store filepath that contains sentence data.', required=True)
	
	result = parser.parse_args()

	if not os.path.exists(result.sentence_path) or os.path.isdir(result.sentence_path):
		print "[ERROR] %s is not a file of sentence data." % (result.sentence_path)
		return

	print "Now doing initialization..."
	
	# initialize processing
	#f = open("/home/gakusei/data/wikipedia/sentences.txt", 'r')
	f = open(result.sentence_path, 'r')
	counter = 0
	while True:
		
		sys.stdout.write("now \"%d\" sentence has been initialized.\r" % counter)
	
		# 1. get input string from standard-input
		line = f.readline()[:-1]
		
		if not line:
			break
	
		obj = init_evaluation_environment(line)
		if obj != None:
	
			# regist Sentence object into global member
			Sentence.append_sentence(obj)
	
			# loop final processing
			counter += 1
	
	f.close()
	
	#
	# Now initialized processing is over, you can compare the similarity of sentence.
	#
	
	print "Initialized processing is over."
	
	for line in sys.stdin:
		line = line[:-1]
		
		if not line:
			break

		print "now processing ..."
	
		#obj = init_evaluation_environment(line, Sentence.generate_id(), relate_similar_words=True)
		obj = init_evaluation_environment(line, relate_similar_words=False)
		if obj != None:
			#Sentence.compare_each_sentences(obj)
			eval_similarity(obj)

		print "...done."

if __name__ == '__main__':
	main()
