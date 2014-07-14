from nltk.corpus import wordnet

#syn_sets = wordnet.synsets('queasy')
#for syn_set in syn_sets:
#	print '%s synonyms:\t%s' % (syn_set, syn_set.lemma_names

def check_synonym(word, word2):
	"""checks to see if word and word2 are synonyms"""
	try:
		
		synsets = wordnet.synsets(word)   #for word1
		for synset in synsets:
			#print synset.lemma_names
			if word2 in synset.lemma_names:
				return 1
		
		synsets2 = wordnet.synsets(word2)   #for word2
		for synset2 in synsets2:
			#print synset.lemma_names
			if word in synset2.lemma_names:
				return 1
				
		return 0
	except:
		return 0
	
'''	
print check_synonym('number','service')
print check_synonym('good','nice')
print check_synonym('numbers','number')
print check_synonym('tag','tree')
print check_synonym('tree','trember')
print check_synonym('window','door')
print check_synonym('pair','two')
print check_synonym('match','twins')
print check_synonym('couple','mates')
print check_synonym('twins','combine')
print check_synonym('team','pair')
'''