from sentence import *

#
# Date      : 2011/08/24
# Author    : Hiroyasu OHYAMA 
# Belonged  : Ariel-Network Inc. (http://www.ariel-networks.com)
#           : Ariel Lab (http://)
# 
# copyright(c) 2011 Hiroyasu OHYAMA. all-right reserved.
#

class Validword:

	# This object ditects sentences that current valid-word has.

	def __init__(self, content):
		self.sentences = []
		self.content = content

	#
	# append sentence-id to object list member of "sentences"
	#
	def add_sentence_id(self, id):
		self.sentences.append(id)

	# This is a debug routine to check the internal of sentence obj
	def get_sentences(self):
		return self.sentences

	# This method is used for searching familar words.
	def get_content(self):
		return self.content

	######
	# following methods are class method.
	###### 

	#
	# This method returns Validword object applied for ditected word of String.
	# And returns None if there is no Validword.
	#
	@classmethod
	def get_wordobj(cls, word):
		ret = None
		if not hasattr(cls, 'dictionary'):
			cls.dictionary = {}
		else:
			if cls.dictionary.has_key(word):
				ret = cls.dictionary[word]

		return ret

	#
	# This method regist word and Validword-object pair onto the class member of dictionary.
	#		returns True if the processing is successfull.
	#		returns False if the same word of String has been already registred.
	#
	@classmethod
	def append_validword(cls, word, validword_obj):
		ret = False

		if not hasattr(cls, 'dictionary'):
			cls.dictionary = {}

		cls.dictionary[word] = validword_obj
		ret = True

		return ret
