#Nov 20, 2013: 
#   improve the program: read myAPITags after tagSet has been constructed. 
#   before: myAPITags and myTagSet are been constructed together, but raw data is so huge, should be this:
#		read each line, and get all tag set with frequency
#		remove the ones with less frequency
#		read each line again, get each API tags 
#	important: in heymann, similarity (bigger it better), in sixuan's similarity (smaller is better). is based on the n_of_apis(tag1) and n_of_apis(tag2),  not the co-occurance graph, 
#
#Nov 19, 2013
#implement original heymann algorithm: for comparison and testing
#differences with sixuan's: 
#   1. unweighted, edges is 1(if co-occurrence greater than a threshold) or 0(if smaller)
#   2. centrality, closeness = 1/some of distances
#   3. similarity cosine K = n(A and B)/square(n(A)* n(B)) 
#
# tag hierarchy learning ;
# myAPITags = get tag of each api with frequency (in its api, line == input output description, line got from tags-part1.py)
# myTagSet = get tag set of all with frequency (total)
# myTagPairs = get tag pair with frequency (in a api line )
# graph = vertice is tag, arch is distance = 1/(frequency *2*3) from myTagPairs
	#1.shortest path in the graph
	#2.lenenshtein
	#3.wordnet similar online
# centrality = sort of closeness in descending order		#	    
#		farness[tag] = costToAll
#		costToAll = sum of distance to all(dijkstra current to each note)
#		closeness[tag] = 1.0/costToAlls
# tag tree builidng:  implement Heymann algorithm # 
# similarity(tag), return most simiar tag, based on 

#@@@Nov 1, 2013: in order to reduce the tag number
#@@@Api remove duplicated tags (optional, not active in this version)
#@@@TagSet Threthold_Tag_Set  remove tagset with lower numbers (single tag not pair) 
#@@@TagPairs Threthold_Tag_Pair  remove TagPairs with lower numbers (pair) 
#@@@centrality  Percentage_2_Remove=0.1 remove 10% tags with lower centrality 

# idea: get tag from centrality, find a similar tag with highest similarity, insert into it as a child (if greater than a threshold) or root (if lower than a threshold)

# readinglist = the count of tag set 

# encoding: UTF-8
import sys
import re


'''main function
inputf = 'taginfo_parsed_1k.txt'
outputfTag = file('tags-tag-140-1k-h.txt', 'w')
outputfGrapgh = file('tags-graph-140-1k-h.txt', 'w')
outputf = file('tags-centrality-140-1k-h.txt', 'w')
outputf2 = file('tags-tree-140-1k-h.txt', 'w')

inputf = 'taginfo-short4test_parsed.txt'
outputfTag = file('tags-tag-140-short-h.txt', 'w')
outputfGrapgh = file('tags-graph-140-short-h.txt', 'w')
outputf = file('tags-centrality-140-short-h.txt', 'w')
outputf2 = file('tags-tree-140-shorts-h.txt', 'w')
'''

#files to save
inputf = '$$all-api-signature.txt'
outputfTag = file('tags-tag-5_2-dot1-h.txt', 'w')
outputfGrapgh = file('tags-graph-5_2-dot1-h.txt', 'w')
outputf = file('tags-centrality-5_2-dot1-h.txt', 'w')
outputf2 = file('tags-tree-5_2-dot1-h.txt', 'w')


#parameters affect the performance
Duplicated_Tags_of_Signature = 1      # whether allowing api signature duplicated (1 allowable; 0 not allowable)
Threthold_Tag_Set = 5                # remove the single tag with lower frequency 
Threthold_Tag_Pair = 2               # if greater than this number, the edge is connected (1) of two tags, otherwise, unconnected (0)
# remove the tag pairs with lower frequency

Centrality_Percentage_2_Remove = 0.1  # remove the tail% of centrality order list
INIT_SIMILARITY_IN_GRAPH = 0          # initial value of he similarity, none similarity (0) infinity (10.0)
THRESHOLD_ADD_TREE_NOTE = 0.2       # whether close enough; if lower, child of root; 
RATIO_LEVENSHTEIN = 0.1               # Similarity_Syntactic; the higher, the more significant
RATIO_SYNONYM = 0.1                   # Similarity_Semantic from wordnet; the higher, the more significant
#SYNONYM_YES_RATIO = 0.2               # Similarity_Semantic, if they are; the lower, the more significant
#SYNONYM_NO_RATIO = 1	              # Similarity_Semantic, if not; the lower, the more significant

#test configuration 
#internet: 1 5 3 0.1 10, 0.1 0.4 0.2 1 
#publication: 1 3 2 0.1 10 0.25 0.5 0.2 1 
#model: 1 3 2 0.1 10 0.25 0.5 0.2 1 
#rest-open: 1 3 2 0.1 10 0.14 0.4 0.2 1 
#All: 1 4 3 0.1 10 0.15 0.5 0.2 1 


MAXLINE = 0 	
myTagSet = {}
myAPITags = [[0 for col in range(MAXLINE)] for row in range(MAXLINE)]  #the 2nd imention is a dict
myTagPairs = {} 

FilterList = set(['all','four','here', 'or','two','more','when','can','one','are','and','have','most','show','there','need','it','in','if','by','up','ad','as','at','no','other'])

lineid = 0

def read_APIs(line):	
	
	global lineid
	
	#API grouped by each line
	lineList = line.split(' ')
	#lineList = line.split('|')
	
	#@@@ improve Nov 1, remove duplicated tags in the signature
	if Duplicated_Tags_of_Signature == 0:
		lineList = sorted(set(lineList),key=lineList.index) 
	
	for word in lineList:
		if len(word) == 0:
			break;
		if len(word) == 1: #filter the word with single letter
			break;
		if word == '\n':
			break;	
		word = word.lower()

		#for counting in TagSet
		if word in myTagSet.keys():
			myTagSet[word] += 1
		else:
			myTagSet[word] = 1
			
	lineid = lineid+1	
	
with open(inputf) as f:
	for line in f:
		read_APIs(line) #parse the line through various functions
	
print "read_APIs for tagSet is done!"




readinglist = {} #for each line

def read_APIs_again(line):	
	
	global readinglist
	global myAPITags
	
	#API grouped by each line
	lineList = line.split(' ')
	#lineList = line.split('|')
	
	#@@@ improve Nov 1, remove duplicated tags in the signature
	if Duplicated_Tags_of_Signature == 0:
		lineList = sorted(set(lineList),key=lineList.index)

	for word in lineList:
		if len(word) == 0:
			break;
		if len(word) == 1: #filter the word with single letter
			break;
		if word == '\n':
			break;	
		#for counting in TagSet
		if word in myTagSet.keys():
			if word in readinglist.keys():
				readinglist[word] += 1
			else:
				readinglist[word] = 1

	if (readinglist):
		taSave = readinglist
		myAPITags.append(taSave)
		readinglist = {}	
		
	
with open(inputf) as f:
	for line in f:
		read_APIs_again(line) #parse the line through various functions
	
print "read_APIs for tagAPIs is done!"



#@@@remove tagset with lower numbers (single tag not pair) Nov 1, 2013
print "len(tagSet)"+"%d" %len(myTagSet)
#Threthold_Tag_Set = 5       #define on the top
tag_set_removed = 0
for (k,v) in myTagSet.items():
	if k in FilterList or v < Threthold_Tag_Set: #Dec 06, delete the ones that not needed
		del myTagSet[k]
		tag_set_removed = tag_set_removed+1

print "tagSet has been shorten!"+ "%d" %tag_set_removed 


#print >> outputfTag, "[TagSet]:"
#for (k,v) in myTagSet.items():
#	print >> outputfTag, "%s:" %k, "%d" %v
	


#print and test
# myAPITags
#print "\nmyAPITags"
#for i_myAPI, myAPI in enumerate(myAPITags):
#	if(myAPI):
#		#print " %d" %i_myAPI
#		for index in myAPI:			
#			print " [%s]=" %index, myAPI[index]
		
# myTagSet		
#print "\nmyTagSet"
#for (k,v) in myTagSet.items():
#	print " [%s] =" % k, v
	
# build myTagPairs
# fix bug: each two tag count twice, the result should be half, Nov 12
# change to use max number for common times of two tags, Nov 12
for myAPI in myAPITags:
	for tag1 in myAPI:	 #for any two in a line 
		for tag2 in myAPI:	
			if(tag1 != tag2):
				pairKey1 = tag1 + "," + tag2
				pairKey2 = tag2 + "," + tag1 
				commonTime = min(myAPI[tag1], myAPI[tag2])
				#commonTime = max(myAPI[tag1], myAPI[tag2])
				if pairKey1 in myTagPairs.keys():
					myTagPairs[pairKey1] += commonTime
				elif pairKey2 in myTagPairs.keys():
					myTagPairs[pairKey2] += commonTime
				else: 
					myTagPairs[pairKey1] = commonTime
					
for (k,v) in myTagPairs.items(): # fix bug: each two tag count twice, the result should be half
	myTagPairs[k] = v/2
	
					
# print myTagPairs
#print "\nmyTagPairs"
#for (k,v) in myTagPairs.items():
#	print " [%s] =" % k, v		

print "myTagPairs is done!"





#@@@remove tagPairs with lower numbers (pair, not single) Nov 1, 2013
print "len(myTagPairs)"+"%d" %len(myTagPairs)
#Threthold_Tag_Pair = 3    #define on the top
tag_pair_removed = 0
for (k,v) in myTagPairs.items():
	if v < Threthold_Tag_Pair:
		del myTagPairs[k]
		tag_pair_removed = tag_pair_removed+1

print "tagPair has been shorten!"+ "%d" %tag_pair_removed

print >> outputfTag, "\n[TagPair]:"
for (k,v) in myTagPairs.items():
	print >> outputfTag, "%s:" %k, "%d" %v



#Dijkstra shortest path
import dijkstra

#tag relations from pairs				
#graph = {
#	'a': {'w': 14, 'x': 7, 'y': 9},
#    'b': {'w': 9, 'z': 6},
#    'w': {'a': 14, 'b': 9, 'y': 2},
#    'x': {'a': 7, 'y': 10, 'z': 15},
#    'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
#    'z': {'b': 6, 'x': 15, 'y': 11},    
#} 

#levenshtein
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]


# build graph
graph = {}
for tag_item in myTagSet:
	graph[tag_item] = {}
	for pair_item in myTagPairs: #get related pairs that contains tag1
		tag_pair = pair_item.split(',')
		tag1 = tag_pair[0]
		tag2 = tag_pair[1]
		
		if(tag1 in myTagSet and tag2 in myTagSet):
			#consider levenshtein
			#lev2 = 0.0
			#lev2 = levenshtein(tag1, tag2)/(1.0*max(len(tag1), len(tag2)))
			
			#consider synonym
			#is_synonym = 0.0
			#if (Synonym.check_synonym (tag1, tag2) == 1):
			#	is_synonym = SYNONYM_YES_RATIO
			#else:
			#	is_synonym = SYNONYM_NO_RATIO		
			
			#if (lev2 == 0.0):
				#likelihoodOfPair = 0.0
			#else: 
				#likelihoodOfPair = 1.0/((1.0)*myTagPairs[pair_item]*lev2*is_synonym) # distance = 1/(frequency * levenshtein * synonym)  ######
			# distance = 
			#1/(frequency * levenshtein * synonym)  ######				
			#format(likelihoodOfPair, '3.8f')	
			
			#for heymann
			#likelihoodOfPair = (1.0)*myTagPairs[pair_item]  #for heymann, likelihoodOfPair = 1
			likelihoodOfPair = 1
			if tag_item == tag_pair[0]: #save the other tag in graph as a edge 
				graph[tag_item][tag_pair[1]] = likelihoodOfPair 
			if tag_item == tag_pair[1]:
				graph[tag_item][tag_pair[0]] = likelihoodOfPair			



#Nov 21, 2013
#if graph[tag_item] = {}, remove this tag_iterm in "graph" and in "tagSet", no need update tagPari, since the graph is from there.
print "len(tagSet)"+"%d" %len(myTagSet)
tag_set_removed = 0
for (k,v) in graph.items():
	if len(v) ==0:  #empty remove  #Nov 29: keep the tags with low frequency,
		#del graph[k] 
		# myTagSet[k]
		tag_set_removed = tag_set_removed+1 


print "tagSet/graph should been shorten but yet "+ "%d" %tag_set_removed 

print >> outputfTag, "[TagSet]:"
for (k,v) in myTagSet.items():
	print >> outputfTag, "%s:" %k, "%d" %v
	

dijkstra.printGraph(graph, outputfGrapgh)  #for printing, show frequent
#dijkstra.printGraphRound(graph, outputfGrapgh)  #the weigh is 1/frequent
			
print "graph building is done!"



# build farness and closeness (sum of distance from each tag to all )	
# will compute distance of two tags (shortest path from each tag to each tag)
#farness = {}
closeness = {}
for item1 in myTagSet:
	costToAll = 0.0
	for item2 in myTagSet:
		cost = dijkstra.shortestPathCost(graph, item1, item2) 
		#print >> outputf, "%3.8f" %(cost), item1, item2, " ->", path 
		#use shortestPath to find path, see dijkstra.py for details
		costToAll += cost
	#farness[item1] = 1.0/costToAll			
	closeness[item1] = 1.0/costToAll #heymann is sum first then reverse, mine is reverse then sum
	#print >> outputf, "closeness:\n ", item1, " -> %3.8f" %(closeness[item1])
	costToAll = 0.0

#print closeness	
#for itemcent in closeness.keys():
#	print itemcent, " -> %3.8f" %(closeness[itemcent])
	
#build centrality (sort of closeness)
centrality = []
centrality = sorted(closeness.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 

#@@@remove 10% tags with lower centrality  (single tag not pair) Nov 1, 2013
#Centrality_Percentage_2_Remove = 0.1    #define in the top
num2Remove = int(len(centrality)*Centrality_Percentage_2_Remove)
for i in range(0,num2Remove):
	del centrality[-1]	


print >> outputf, "\ncentrality decreasing tag list (with" + "%d" %num2Remove + " tags removed):"
for centr in centrality:		
	print >> outputf, "[%s]=" %centr[0], "->", centr[1]





#part 3: build tree
# implement Heymann algorithm # 
# tagTree = [{'tag1,tag2':score}]
# centrality = sort of closeness in descending order
# myTagSet = get tag set of all with frequency (total)
# graph = vertice is tag, arch is distance = 1/frequency from myTagPairs
# similarity(tag), return most simiar tag, based on 
	#1.shortest path in the graph
	#2.lenenshtein
	#3.wordnet similar online
# idea: get tag from centrality, find a similar tag with highest similarity, insert into it as a child (if greater than a threshold) or root (if lower than a threshold)


# define on the top
#INIT_SIMILARITY_IN_GRAPH = 10.0
#THRESHOLD_ADD_TREE_NOTE = 0.25 # whether close enough, the smaller the better
##RATIO_DISTANCE = 0.5 #no need ratio, bacause we are multiplying
#RATIO_LEVENSHTEIN = 0.25
##RATIO_SYNONYM = 0.0
#SYNONYM_YES_RATIO = 0.3
#SYNONYM_NO_RATIO = 1	

#find lowest similarity tag in the graph
def tag_with_lowest_similarity_graph_distance(tag_in_set):
	if(tag_in_set in myTagSet):
		similar_tag = ''
		similar_cost_last = INIT_SIMILARITY_IN_GRAPH
		for item1 in myTagSet:
			if (items != tag_in_set):
				similar_cost = dijkstra.shortestPathCost(graph, tag_in_set, item1)
				if (similar_cost<similar_cost_last):
					similar_tag = item1
					similar_cost_last = similar_cost
		return similar_tag, similar_cost_last
	else:
		return '', INIT_SIMILARITY_IN_GRAPH
		
#find lowest similarity tag in the tree
def graph_distance(tag1, tag2):
	if(tag1 in myTagSet and tag2 in myTagSet):
		return dijkstra.shortestPathCost(graph, tag1, tag2)		
	else:
		return INIT_SIMILARITY_IN_GRAPH

import tree
from sys import argv

import SynonymWordnet
#import Synonym
#SYNONYM_YES_RATIO = 0.3
#SYNONYM_NO_RATIO = 1	
	
#similarity cosine K = n(A and B)/square(n(A)* n(B)),   squaring is v2**(1.0/2)   
	#read each line of tags-tag-140-2k.txt
	#count line number of # the total number of apis that satisfies
	#	num_both = both has tag A and tag B
	#	num_taga = has tag A
	#	num_tagb = has tag B
def similarity_tags_heymann(tag1, tag2):	

	#if the tag1 and tag2 not co-existed for the threthold of APIpairs, (that is to say they are not in the tagPairs, the similarity is 0)

	pairKey1 = tag1 + "," + tag2
	pairKey2 = tag2 + "," + tag1 
	if pairKey1 not in myTagPairs.keys() and pairKey2 not in myTagPairs.keys():
		return INIT_SIMILARITY_IN_GRAPH				
	else: 
		num_both = 0
		num_taga = 0
		num_tagb = 0
		for myAPI in myAPITags:
			if tag1 in myAPI.keys() and tag2 in myAPI.keys():	 #for any two in a line #myAPI[tag1]  #if tag_name in readinglist.keys():
				num_both+=1
				num_taga+=1
				num_tagb+=1
			else: 
				if tag1 in myAPI.keys():
					num_taga+=1
				if tag2 in myAPI.keys():
					num_tagb+=1
			
		toBeDivided = num_taga*num_tagb
		toBeDivided = toBeDivided**(1.0/2)   
		#print tag1," and ", tag2," simi: ", "%3.8f" %(1.0*num_both/toBeDivided)
		return 1.0*num_both/toBeDivided
			
	
import PathSimilarity

#similarity of two tags, includes three methods: 1. graph_distance 2. sentence levenshtein (* Nlevij) 3. similar word, similarity of wordnet synonym list
def similarity_tags_sixuan(tag1, tag2):
	#Nlevij = levij/max(length(ti),length(tj)). the smaller the better
	#multiple Nlevij to graph_distance
	v1 = graph_distance(tag1, tag2)
	v2 = 0.0
	v2 = levenshtein(tag1, tag2)/(1.0*max(len(tag1), len(tag2)))
	#v2 = n + (1-n)*lev/max(len1,len2)
	v2 = (1- RATIO_LEVENSHTEIN) + RATIO_LEVENSHTEIN * v2
	#10,10,2013 try the multiply, performance is bad, the scale of v1 and v2 are not the same
	#print >> outputf, "v2 %3.8f" %(v2), "| tag:", tag1, "| tagto: ", tag2
	
	#consider synonym
	#is_synonym = 0.0
	#if (SynonymWordnet.check_synonym (tag2, tag1) == 1):
	#	is_synonym = SYNONYM_YES_RATIO
	#else:
	#	is_synonym = SYNONYM_NO_RATIO
		
		
	#test3: get the similarity semantic of two tags, use path similarity of wordnet
	sim_synonym =  PathSimilarity.pathSimilarity(tag1, tag2)
	
	v3 = (1-RATIO_SYNONYM) + RATIO_SYNONYM * (1-sim_synonym) #originally, the sim_synonym is [0,1], the more close, more higher; for sixuan's, it should be 1-sim_synonym, since sixuan's, the smaller the better; then multifly the ratio
	
	if(v2 != 0.0):
		v1=v1*v2
	if(v3 != 0.0):
		v1=v1*v3
	return v1

	
if __name__ == '__main__':

	print >> outputf
	
	tagTree = tree.Tree()
	tagTree.create_node(INIT_SIMILARITY_IN_GRAPH,'treeRoot') #root
	
	treeTags = [] #tags already in the list
	
	for tagInCentrality in centrality: #tagCandidate[0] is tag that wants to add in the tree, WARNING: should be tagCandidate
		tagCandidate = tagInCentrality[0]
		similarity = INIT_SIMILARITY_IN_GRAPH
		tagToAttach = 'treeRoot'
		if(treeTags): #when tree has tags rather than root
			for tagInTree in treeTags: #find a closest one in the tree
				#similarity function needed: input(tagCandidate,tagInTree), output(similarity) the bigger the better
				similarity_new = similarity_tags_heymann(tagCandidate,tagInTree)
				
				#print similarity_new, "| tag:", tagCandidate, "| tagto: ", tagInTree
				#print "new : ", similarity_new, "old", similarity, "compare:" , (similarity_new < similarity)
				#if(similarity_new < similarity):
				if(similarity_new > similarity):
					similarity = similarity_new #node data
					tagToAttach = tagInTree      #node parent
			
			print >> outputf, "similarity: %3.8f" %(similarity), "| tag:", tagCandidate, "| tagto: ", tagToAttach					
			#if (similarity < THRESHOLD_ADD_TREE_NOTE): #if the closest one is close enough
			if (similarity > THRESHOLD_ADD_TREE_NOTE): #if the closest one is close enough
				tagTree.create_node(similarity, tagCandidate, parent = tagToAttach)				
			else: 			#new node add to root
				tagTree.create_node(similarity, tagCandidate, parent = 'treeRoot')			
		else:  #when tree is empty
			tagTree.create_node(similarity, tagCandidate, parent = 'treeRoot')
			
		treeTags.append(tagCandidate)
	#print tree		

	tagTree.show('treeRoot',outputf2)		

				
	print "tree learning is done!"
	
	outputf.close()
	outputf2.close()
	outputfTag.close()
	outputfGrapgh.close()
	
	print "all done!"
			
#test tagTree
#print "\ntagTree"
#for (k,v) in tagTree.items():
#	print k, ': '
#	for (k2,v2) in tagTree[k].items():
#		print k2, ',', v2, ';'



