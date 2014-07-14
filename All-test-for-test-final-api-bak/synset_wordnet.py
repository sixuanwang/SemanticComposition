from nltk.corpus import wordnet as wn

'''
synsets = wn.synsets('dog')   #for word1
for synset in synsets:
	print synset.lemma_names

'''
#dog = wn.synset('dog.n.01')
#cat = wn.synset('cat.n.01')

synsets1 = wn.synsets('music')   #for word1
synsets2 = wn.synsets('mp3')   #for word1

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
		
print "Size:",    len(similarity_list)  if len(similarity_list) > 0 else float('nan')
print "Min:",     min(similarity_list)  if len(similarity_list) > 0 else float('nan')
print "Max:",     max(similarity_list)  if len(similarity_list) > 0 else float('nan')
print "Average:", float(sum(similarity_list))/len(similarity_list) if len(similarity_list) > 0 else float('nan')

