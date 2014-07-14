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
inputf = file('publication-after-part1.txt')
outputf = file('tags-centrality-simmore123-publication.txt', 'w')
outputf2 = file('tags-tree-simmore123-publication.txt', 'w')
'''

#files to save
inputf = file('All-api-signature.txt')
outputfTag = file('tags-tag-simmore123v2-All.txt', 'w')
outputfGrapgh = file('tags-graph-simmore123v2-All.txt', 'w')
outputf = file('tags-centrality-simmore123v2-All.txt', 'w')
outputf2 = file('tags-tree-simmore123v2-All.txt', 'w')

#parameters affect the performance
Duplicated_Tags_of_Signature = 1      # whether allowing api signature duplicated (1 allowable; 0 not allowable)
Threthold_Tag_Set = 1                 # remove the single tag with lower frequency 
Threthold_Tag_Pair = 3                # remove the tag pairs with lower frequency

Centrality_Percentage_2_Remove = 0.1  # remove the tail% of centrality order list
INIT_SIMILARITY_IN_GRAPH = 10.0       # initial value of he similarity, infinity
THRESHOLD_ADD_TREE_NOTE = 0.15         # whether close enough; if lower, child of root; 
RATIO_LEVENSHTEIN = 0.5               # Similarity_Syntactic; the higher, the more significant
SYNONYM_YES_RATIO = 0.2               # Similarity_Semantic, if they are; the lower, the more significant
SYNONYM_NO_RATIO = 1	              # Similarity_Semantic, if not; the lower, the more significant

#test configuration 
#internet: 1 5 3 0.1 10, 0.1 0.4 0.2 1 
#publication: 1 3 2 0.1 10 0.25 0.5 0.2 1 
#model: 1 3 2 0.1 10 0.25 0.5 0.2 1 
#rest-open: 1 3 2 0.1 10 0.14 0.4 0.2 1 
#All: 1 4 3 0.1 10 0.15 0.5 0.2 1 


MAXLINE = 0 	
myAPITags = [[0 for col in range(MAXLINE)] for row in range(MAXLINE)]   
myTagSet = {}
myTagPairs = {}

lineid = 0
readinglist = {} #for each line


def read_APIs(line):	
	
	global readinglist
	global myAPITags
	global lineid
	
	#API grouped by each line
	lineList = line.split(' ')
	
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



#@@@remove tagset with lower numbers (single tag not pair) Nov 1, 2013
print "len(tagSet)"+"%d" %len(myTagSet)
#Threthold_Tag_Set = 5       #define on the top
tag_set_removed = 0
for (k,v) in myTagSet.items():
	if v < Threthold_Tag_Set:
		del myTagSet[k]
		tag_set_removed = tag_set_removed+1 

print "tagSet has been shorten!"+ "%d" %tag_set_removed 

print >> outputfTag, "[TagSet]:"
for (k,v) in myTagSet.items():
	print >> outputfTag, "%s:" %k, "%d" %v

outputfTag.close()
print "all done!"
		

   

