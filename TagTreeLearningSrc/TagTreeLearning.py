#July 9, 2014: 
#	test for DEVS models, learn tag from the tag I get from the Model of list website, 
#	IMPORTENT: if the input has the tags of each resource in a line, this program will split them and learn their tag tree 
#	restructure and prepare for the project refinement. 

#Nov 20, 2013: 
#   improve the program: read myAPITags after tagSet has been constructed. 
#   before: myAPITags and myTagSet are been constructed together, but raw data is so huge, should be this:
#		read each line, and get all tag set with frequency
#		remove the ones with less frequency
#		read each line again, get each API tags 
 
# tag hierarchy learning ;
# myAPITags = get tag of each api with frequency (in its api, line == input output description, line got from tags-part1.py)
# myTagSet = get tag set of all with frequency (total)
# myTagPairs = get tag pair with frequency (in a api line )
# graph = vertice is tag, arch is distance = 1/(frequency) from myTagPairs

# tag tree building (centrality function to select tag):  implement Heymann algorithm # 
# centrality = sort of closeness in descending order		#	    
#		costToAll = sum of distance to all(dijkstra current to each note)
#		closeness[tag] = costToAlls
#		farness[tag] = 1/costToAll
# similarity function (to place tag), return most similar tag, based on (distance, syntactic, semantic)
	#1.shortest path in the graph
	#2.lenenshtein
	#3.wordnet similarity

#@@@Nov 1, 2013: in order to reduce the tag number
#@@@Api remove duplicated tags (optional, not active in this version)
#@@@TagSet Threthold_Tag_Set  remove tagset with lower numbers (single tag not pair) 
#@@@TagPairs Threthold_Tag_Pair  remove TagPairs with lower numbers (pair) 
#@@@centrality  Percentage_2_Remove=0.1 remove 10% tags with lower centrality 
# idea: get tag from centrality, find a similar tag with highest similarity, insert into it as a child (if greater than a threshold) or root (if lower than a threshold)
# readinglist = the count of tag set 


import sys
import re


#files to save
inputf = 'ExtractDEVSModelResults-NamePorts-selected-supposed-generated-v2 - manual tag.txt'
outputfTag = file('tags-tag-073.txt', 'w')
outputfGrapgh = file('tags-graph-073.txt', 'w')
outputCentralityList = file('tags-centrality-073.txt', 'w')
outputfTree = file('tags-tree-073.txt', 'w')

#parameters affect the performance
Allow_Duplicated_Tags_of_Signature = 0      # whether allowing api signature duplicated (1 allowable; 0 not allowable)
Threthold_Tag_Set = 7               # remove the single tag with lower frequency 
Threthold_Tag_Pair = 3                # remove the tag pairs with lower frequency

Centrality_Percentage_2_Remove = 0.1  # remove the tail% of centrality order list
INIT_SIMILARITY_IN_GRAPH = 10          # initial value of similarity, none similarity (0) infinity (10.0)
THRESHOLD_ADD_TREE_NOTE = 0.2         # whether close enough; if lower, child of root; 
RATIO_LEVENSHTEIN = 0.1               # Similarity_Syntactic; the higher, the more significant
RATIO_SYNONYM = 0.1                   # Similarity_Semantic from wordnet; the higher, the more significant



MAXLINE = 0 
myAPIlist = []  #all lines with original tags for each line
myTagSet = {}  #myTagSet[word] += 1, so for each word, it is ['tag']= number
myAPITags = [[0 for col in range(MAXLINE)] for row in range(MAXLINE)]  # is an arraylist of lines, for each line is a TagSet [{['tag']= number...}, {}, {}]
myTagPairs = {} #myTagPairs[pairKey1] += 1, so for each pair, it is ['tag1', '->', 'tag2']= number

FilterList = set(['all','four','here', 'or','two','more','when','can','one','are','and','have','most','show','there','need','it','in','if','by','up','ad','as','at','no','other'])

def read_APIs(line):  
	if (len(line.split('|'))!= 4 ): #get all tags
		return
	else:
		lineRead = []   #put them together
		lineRead = re.split(' |_', line)
	
		myAPIlist.append(lineRead)
				

def getMyTagSet(myAPIlist):	
	readinglist = {} #for each line
	for lineRead in myAPIlist:
		#@@@ improve Nov 1, remove duplicated tags in the signature
		if Allow_Duplicated_Tags_of_Signature == 0:
			lineRead = sorted(set(lineRead),key=lineRead.index) 
			
		while('' in lineRead):
			lineRead.remove('')
		while('|' in lineRead):
			lineRead.remove('|')
		while('\n' in lineRead):
			lineRead.remove('\n')
		
		for word in lineRead:
			word = word.lower()
			if '\n' in word or word == '' or word == '|':
				break;	
			if word in myTagSet.keys():
				if word in readinglist.keys():
					readinglist[word] += 1
				else:
					readinglist[word] = 1
				myTagSet[word] += 1
			else:
				myTagSet[word] = 1
		
		if (readinglist):
			taSave = readinglist
			myAPITags.append(taSave)
			readinglist = {}	
		
with open(inputf) as f:
	for line in f:
		read_APIs(line) #parse the line through various functions

getMyTagSet(myAPIlist)
	
print "read_APIs for tagSet is done!"		
print "read_APIs for tagAPIs is done!"


#@@@remove tagset with lower numbers (single tag not pair) Nov 1, 2013
print "len(tagSet)"+"%d" %len(myTagSet)
tag_set_removed = 0
for (k,v) in myTagSet.items():
	if k in FilterList or v < Threthold_Tag_Set: #Dec 06 , delete the ones that not needed
		del myTagSet[k]
		tag_set_removed = tag_set_removed+1 

print "tagSet has been shorten!"+ "%d" %tag_set_removed 

	
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
	
print "myTagPairs is done!"


#@@@remove tagPairs with lower numbers (pair, not single) Nov 1, 2013
print "len(myTagPairs)"+"%d" %len(myTagPairs)
#Threthold_Tag_Pair = 3    #define on the top
tag_pair_removed = 0
for (k,v) in myTagPairs.items():
	if v < Threthold_Tag_Pair:
		del myTagPairs[k]
		tag_pair_removed = tag_pair_removed+1

print "tagPair need has been shorten!"+ "%d" %tag_pair_removed



# print test, uncomment the below for printing
#print >> outputfTag, "[TagSet]:"
#for (k,v) in myTagSet.items():
#	print >> outputfTag, " [%s] =" % k, v
	
#print >> outputfTag, "\n[myAPITags]"
#for i_myAPI, myAPI in enumerate(myAPITags):
#	if(myAPI):
#		print >> outputfTag, " %d" %i_myAPI
#		for index in myAPI:			
#			print >> outputfTag, " [%s]=" %index, myAPI[index]	

#print >> outputfTag,  "\n[myTagPairs]"
#for (k,v) in myTagPairs.items():
#	print >> outputfTag,  " [%s] =" % k, v	


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
			likelihoodOfPair = 1.0/((1.0)*myTagPairs[pair_item]) # distance = 1/(frequency * levenshtein * synonym)  ######
				
			#format(likelihoodOfPair, '3.8f')
			if tag_item == tag_pair[0]: #save the other tag in graph as a edge 
				graph[tag_item][tag_pair[1]] = likelihoodOfPair 
			if tag_item == tag_pair[1]:
				graph[tag_item][tag_pair[0]] = likelihoodOfPair			


#Nov 21, 2013
#if graph[tag_item] = {}, remove this tag_iterm in "graph" and in "tagSet", no need update tagPair, since the graph is from tagPair.
print "len(tagSet)"+"%d" %len(myTagSet)
tag_set_removed = 0
for (k,v) in graph.items():
	if len(v) ==0:  #empty remove #Nov 29: keep the tags with low frequency,
		#del graph[k]
		#del myTagSet[k]
		tag_set_removed = tag_set_removed+1 

print "tagSet/graph has been shorten "+ "%d" %tag_set_removed 

print >> outputfTag, "[TagSet]:"
for (k,v) in myTagSet.items():
	print >> outputfTag, "%s:" %k, "%d" %v
	
#Nov 26, 2013
#in sixuan's algorithm, in graph, if two tags are not connected, should have a weight of 1
for (k,v) in graph.items():
	for tag_item in myTagSet:
		if(tag_item != k and tag_item not in graph[k].keys()):
			graph[k][tag_item] = 1	

	
#dijkstra.printGraph(graph, outputfGrapgh)  #the weigh is 1/frequent
dijkstra.printGraphRound(graph, outputfGrapgh)  #for printing, show frequent
			
print "graph building is done!"

	
#### SIXUAN-to do: here is claculateCentrality, extract to a function
# build farness and closeness (sum of distance from each tag to all )	
# will compute distance of two tags (shortest path from each tag to each tag)
#farness = {}
closeness = {}
for item1 in myTagSet:
	costToAll = 0.0
	for item2 in myTagSet:
		cost = dijkstra.shortestPathCost(graph, item1, item2) 
		#print >> outputCentralityList, "%3.8f" %(cost), item1, item2, " ->", path 
		#use shortestPath to find path, see dijkstra.py for details
		costToAll += cost
	#farness[item1] = 1.0/costToAll			
	closeness[item1] = costToAll
	#print >> outputCentralityList, "closeness:\n ", item1, " -> %3.8f" %(closeness[item1])
	costToAll = 0.0

#print closeness	
#for itemcent in closeness.keys():
#	print itemcent, " -> %3.8f" %(closeness[itemcent])
	
#build centrality (sort of closeness)
centrality = []
centrality = sorted(closeness.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)

#@@@remove 10% tags with lower centrality  (single tag not pair) Nov 1, 2013
#Centrality_Percentage_2_Remove = 0.1    #define in the top
num2Remove = int(len(centrality)*Centrality_Percentage_2_Remove)
for i in range(0,num2Remove):
	del centrality[-1]	


print >> outputCentralityList, "\ncentrality decreasing tag list (with" + "%d" %num2Remove + " tags removed):"
for centr in centrality:		
	print >> outputCentralityList, "[%s]=" %centr[0], "->", centr[1]



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
#1. graph_distance
def graph_distance(tag1, tag2):
	if(tag1 in myTagSet and tag2 in myTagSet):
		return dijkstra.shortestPathCost(graph, tag1, tag2)		
	else:
		return INIT_SIMILARITY_IN_GRAPH

import tree
from sys import argv

import SynonymWordnet
import PathSimilarity
#import Synonym
#SYNONYM_YES_RATIO = 0.3
#SYNONYM_NO_RATIO = 1	
	
##SIXUAN: NEED TO SEPERATE THE FUNCTION 2 AND FUNCTION 3.

#similarity of two tags, includes three methods: 1. graph_distance 2. sentence levenshtein (* Nlevij) 3. similar word (* 0.2-RATIO if similar)
def calculateSimilarity(tag1, tag2):
	#Nlevij = levij/max(length(ti),length(tj)). the smaller the better
	#multiple Nlevij to graph_distance
	v1 = graph_distance(tag1, tag2)
	v2 = 0.0
	v2 = levenshtein(tag1, tag2)/(1.0*max(len(tag1), len(tag2)))
	#v2 = n + (1-n)*lev/max(len1,len2)
	v2 = (1- RATIO_LEVENSHTEIN) + RATIO_LEVENSHTEIN * v2
	sim_synonym =  PathSimilarity.pathSimilarity(tag1, tag2)
	
	v3 = (1-RATIO_SYNONYM) + RATIO_SYNONYM * (1-sim_synonym) #originally, the sim_synonym is [0,1], the more close, more higher; for sixuan's, it should be 1-sim_synonym, since sixuan's, the smaller the better; then multifly the ratio
	
	if(v2 != 0.0):
		v1=v1*v2
	if(v3 != 0.0):
		v1=v1*v3
	return v1

	
#### SIXUAN-to do: here is treeLearningProcess, extract to a function
if __name__ == '__main__':
	print >> outputCentralityList
	
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
				similarity_new = calculateSimilarity(tagCandidate,tagInTree)
				
				#print similarity_new, "| tag:", tagCandidate, "| tagto: ", tagInTree
				#print "new : ", similarity_new, "old", similarity, "compare:" , (similarity_new < similarity)
				if(similarity_new < similarity):
					similarity = similarity_new #node data
					tagToAttach = tagInTree      #node parent
			
			print >> outputCentralityList, "similarity: %3.8f" %(similarity), "| tag:", tagCandidate, "| tagto: ", tagToAttach					
			if (similarity < THRESHOLD_ADD_TREE_NOTE): #if the closest one is close enough
				tagTree.create_node(similarity, tagCandidate, parent = tagToAttach)				
			else: 			#new node add to root
				tagTree.create_node(similarity, tagCandidate, parent = 'treeRoot')			
		else:  #when tree is empty
			tagTree.create_node(similarity, tagCandidate, parent = 'treeRoot')
			
		treeTags.append(tagCandidate)
	#print tree		

	tagTree.show('treeRoot',outputfTree)		

				
	print "tree learning is done!"
	
	outputCentralityList.close()
	outputfTree.close()
	outputfTag.close()
	outputfGrapgh.close()
	
	print "all done!"
