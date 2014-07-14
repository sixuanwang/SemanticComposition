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

# idea: get tag from centrality, find a similar tag with highest similarity, insert into it as a child (if greater than a threshold) or root (if lower than a threshold)

# encoding: UTF-8
import sys
import re


'''main function
inputf = file('publication-after-part1.txt')
outputf = file('tags-centrality-simmore123-publication.txt', 'w')
outputf2 = file('tags-tree-simmore123-publication.txt', 'w')
'''
MAXLINE = 0 	
myAPITags = [[0 for col in range(MAXLINE)] for row in range(MAXLINE)]   
myTagSet = {}
myTagPairs = {}

inputf = file('model-after-part1.txt')
outputf = file('tags-centrality-simmore123-model.txt', 'w')
outputf2 = file('tags-tree-simmore123-model.txt', 'w')
lineid = 0
readinglist = {} #for each line


def read_APIs(line):	
	
	global readinglist
	global myAPITags
	global lineid
	
	#API grouped by each line
	lineList = line.split(' ')
	for word in lineList:
		if len(word) == 0:
			break;
		if len(word) == 1: #filter the word with single letter
			break;
		if word == '\n':
			break;		
		#for counting in APItags
		if word in readinglist.keys():
			readinglist[word] += 1
		else:
			readinglist[word] = 1
		#for counting in TagSet
		if word in myTagSet.keys():
			myTagSet[word] += 1
		else:
			myTagSet[word] = 1
		
	lineid = lineid+1
	#print "lineID: %d" % lineid
	#for (k,v) in readinglist.items():
		#print " [%s] =" % k, v
	if (readinglist):
		taSave = readinglist
		myAPITags.append(taSave)
		readinglist = {}		
	
	
	'''
	#API grouped by empty line
	if (line[:-1].strip()): #still in an api, reading, and record frequency
		lineList = line.split(' ')
		for word in lineList:
			if len(word) == 0:
				break;
			if word == '\n':
				break;		
			#for counting in APItags
			if word in readinglist.keys():
				readinglist[word] += 1
			else:
				readinglist[word] = 1
			#for counting in TagSet
			if word in myTagSet.keys():
				myTagSet[word] += 1
			else:
				myTagSet[word] = 1
	else: #end of an api, save
		lineid = lineid+1
		#print "lineID: %d" % lineid
		#for (k,v) in readinglist.items():
			#print " [%s] =" % k, v
		if (readinglist):
			taSave = readinglist
			myAPITags.append(taSave)
			readinglist = {}
	'''
while True:
	line = inputf.readline()
	
	read_APIs(line) #parse the line through various functions
	
	if not line:
		break
	
inputf.close()

print "read_APIs is done!"

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
for myAPI in myAPITags:
	for tag1 in myAPI:	
		for tag2 in myAPI:	
			if(tag1 != tag2):
				pairKey1 = tag1 + "," + tag2
				pairKey2 = tag2 + "," + tag1 
				commonTime = min(myAPI[tag1], myAPI[tag2])
				if pairKey1 in myTagPairs.keys():
					myTagPairs[pairKey1] += commonTime
				elif pairKey2 in myTagPairs.keys():
					myTagPairs[pairKey2] += commonTime
				else: 
					myTagPairs[pairKey1] = commonTime
					
# print myTagPairs
#print "\nmyTagPairs"
#for (k,v) in myTagPairs.items():
#	print " [%s] =" % k, v		

print "myTagPairs is done!"


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
		likelihoodOfPair = 1.0/((1.0)*myTagPairs[pair_item]) # distance = 1/(frequency * levenshtein * synonym)  ######
			
		#format(likelihoodOfPair, '3.8f')
		if tag_item == tag_pair[0]: #save the other tag in graph as a edge 
			graph[tag_item][tag_pair[1]] = likelihoodOfPair 
		if tag_item == tag_pair[1]:
			graph[tag_item][tag_pair[0]] = likelihoodOfPair
			
			
print "graph building is done!"




# build farness and closeness (sum of distance from each tag to all )	
# will compute distance of two tags (shortest path from each tag to each tag)
farness = {}
closeness = {}
for item1 in myTagSet:
	costToAll = 0.0
	for item2 in myTagSet:
		cost = dijkstra.shortestPathCost(graph, item1, item2) 
		#print >> outputf, "%3.8f" %(cost), item1, item2, " ->", path 
		#use shortestPath to find path, see dijkstra.py for details
		costToAll += cost
	farness[item1] = costToAll			
	closeness[item1] = 1.0/costToAll
	#print >> outputf, "closeness:\n ", item1, " -> %3.8f" %(closeness[item1])
	costToAll = 0.0

#print closeness	
#for itemcent in closeness.keys():
#	print itemcent, " -> %3.8f" %(closeness[itemcent])
	
#build centrality (sort of closeness)
centrality = []
centrality = sorted(closeness.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

print >> outputf, "\ncentrality decreasing tag list: "
for centr in centrality:		
	print >> outputf, "[%s]=" %centr[0], "->", centr[1]




'''
part 3: build tree
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
'''	

INIT_SIMILARITY_IN_GRAPH = 10.0
THRESHOLD_ADD_TREE_NOTE = 0.25 # whether close enough, the smaller the better
#RATIO_DISTANCE = 0.5 #no need ratio, bacause we are multiplying
RATIO_LEVENSHTEIN = 0.25
RATIO_SYNONYM = 0.0

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
SYNONYM_YES_RATIO = 0.3
SYNONYM_NO_RATIO = 1	
	

#similarity of two tags, includes three methods: 1. graph_distance 2. sentence levenshtein (* Nlevij) 3. similar word (* 0.2-RATIO if similar)
def similarity_tags(tag1, tag2):
	#Nlevij = levij/max(length(ti),length(tj)). the smaller the better
	#multiple Nlevij to graph_distance
	v1 = graph_distance(tag1, tag2)
	v2 = 0.0
	v2 = levenshtein(tag1, tag2)/(1.0*max(len(tag1), len(tag2)))
	#v2 = n + (1-n)*lev/max(len1,len2)
	v2 = 1- RATIO_LEVENSHTEIN + RATIO_LEVENSHTEIN*v2
	#10,10,2013 try the multiply, performance is bad, the scale of v1 and v2 are not the same
	print >> outputf, "v2 %3.8f" %(v2), "| tag:", tag1, "| tagto: ", tag2
	
	#consider synonym
	is_synonym = 0.0
	if (SynonymWordnet.check_synonym (tag2, tag1) == 1):
		is_synonym = SYNONYM_YES_RATIO
	else:
		is_synonym = SYNONYM_NO_RATIO
		
	if (v2 != 0.0):
		#v2 = v2**(1.0/2) #too large last time, make squaring
		return v1*v2*is_synonym
	else:
		return v1*is_synonym

	
if __name__ == '__main__':


	tagTree = tree.Tree()
	tagTree.create_node(INIT_SIMILARITY_IN_GRAPH,'root') #root
	
	treeTags = [] #tags already in the list
	
	for tagInCentrality in centrality: #tagCandidate[0] is tag that wants to add in the tree, WARNING: should be tagCandidate
		tagCandidate = tagInCentrality[0]
		similarity = INIT_SIMILARITY_IN_GRAPH
		tagToAttach = 'root'
		if(treeTags): #when tree has tags rather than root
			for tagInTree in treeTags: #find a closest one in the tree
				#similarity function needed: input(tagCandidate,tagInTree), output(similarity) the bigger the better
				similarity_new = similarity_tags(tagCandidate,tagInTree)
				
				#print similarity_new, "| tag:", tagCandidate, "| tagto: ", tagInTree
				#print "new : ", similarity_new, "old", similarity, "compare:" , (similarity_new < similarity)
				if(similarity_new < similarity):
					similarity = similarity_new #node data
					tagToAttach = tagInTree      #node parent
			
			print >> outputf, "similarity: %3.8f" %(similarity), "| tag:", tagCandidate, "| tagto: ", tagToAttach					
			if (similarity < THRESHOLD_ADD_TREE_NOTE): #if the closest one is close enough
				tagTree.create_node(similarity, tagCandidate, parent = tagToAttach)				
			else: 			#new node add to root
				tagTree.create_node(similarity, tagCandidate, parent = 'root')			
		else:  #when tree is empty
			tagTree.create_node(similarity, tagCandidate, parent = 'root')
			
		treeTags.append(tagCandidate)
	#print tree		

	tagTree.show('root',outputf2)		

	outputf.close()
	outputf2.close()
	
	

			
#test tagTree
#print "\ntagTree"
#for (k,v) in tagTree.items():
#	print k, ': '
#	for (k2,v2) in tagTree[k].items():
#		print k2, ',', v2, ';'





   

