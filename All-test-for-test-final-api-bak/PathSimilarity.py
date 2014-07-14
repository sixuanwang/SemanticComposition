from nltk.corpus import wordnet as wn

def pathSimilarity(word1,word2):
	synsets1 = wn.synsets(word1)   #for word1
	synsets2 = wn.synsets(word2)   #for word1

	synset_average = 0.0
	synset_max = 0.0
	synset_min = 0.0
	synset_sum = 0.0
	synset_num = 0

	similarity_list =[]

	for synset in synsets1:
		for synset2 in synsets2:
			this_similarity = synset.path_similarity(synset2)
			if(this_similarity>0):
				similarity_list.append(this_similarity)
		
	return max(similarity_list)  if len(similarity_list) > 0 else float(0.0)

print pathSimilarity('man','human')
'''	
	print "Size:",    len(similarity_list)  if len(similarity_list) > 0 else float(0.0)
	print "Min:",     min(similarity_list)  if len(similarity_list) > 0 else float(0.0)
	print "Max:",     max(similarity_list)  if len(similarity_list) > 0 else float(0.0)
	print "Average:", float(sum(similarity_list))/len(similarity_list) if len(similarity_list) > 0 else float(0.0)
'''
