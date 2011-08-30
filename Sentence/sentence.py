import math

#
# Date      : 2011/08/24
# Author    : Hiroyasu OHYAMA 
# Belonged  : Ariel-Network Inc. (http://www.ariel-networks.com)
#           : Ariel Lab (http://)
# 
# copyright(c) 2011 Hiroyasu OHYAMA. all-right reserved.
#

from word import *

class Sentence:

	# The id has to be more than 1, because 0 means error id.
	def __init__(self, content):
		self.id = self.generate_id()
		self.words = {}
		self.content = content

	def get_content(self):
		return self.content

	def get_wordlist(self):
		wordlist = []
		for word in self.words:
			obj = Validword.get_wordobj(word)

			if obj != None:
				wordlist.append(obj)

		return wordlist

	# return id number, 0 means error.
	def get_id(self):
		ret = 0
		if hasattr(self, 'id'):
			ret = self.id

		return ret

	# regist valid word
	def regist_word(self, word):

		if not self.words.has_key(word):
			self.words[word] = 0

		self.words[word] += 1

	def get_word_count(self, word):
		ret = 0
		if self.words.has_key(word):
			ret = self.words[word]

		return ret

	# This routine calculate scala size of feature vector of current object
	def scale_vector(self):
		scala = 0
		for word in self.words.keys():
			scala += math.pow(self.words[word], 2)

		return math.sqrt(scala)

	# This routine calculate similar degree using Vector Space Model
	def similar_degree(self, compare):
		retval = 0
		current_scala = self.scale_vector()
		compare_scala = compare.scale_vector()

		for word in self.words:
			compare_count = compare.get_word_count(word)
			if compare_count != 0:
				retval += self.words[word] * compare_count

		return retval / (current_scala * compare_scala)

	######
	# following methods are class method.
	###### 

	@classmethod
	def __get_all(cls):
		if not hasattr(cls, 'total_list'):
			cls.total_list = []

		return cls.total_list

	@classmethod
	def append_sentence(cls, sentence):
		if not hasattr(cls, 'total_list'):
			cls.total_list = []

		return cls.total_list.append(sentence)

	@classmethod
	def compare_each_sentences(cls, sentence):
		for item in cls.__get_all():
			print "[compare_each_sentences] %s : %f" % (item.get_content(), sentence.similar_degree(item))

	@classmethod
	def getobj_from_id(cls, id):
		retobj = None
		#if not index >= len(cls.__get_all()) and index >= 0:
		for item in cls.__get_all():
			if item.get_id() == id:
				retobj = item
				break

		return retobj
	
	@classmethod
	def generate_id(cls):
		return len(cls.__get_all()) + 1
