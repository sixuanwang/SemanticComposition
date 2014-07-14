#Nov 21, 2013: 
#find composible apis 
#do the test of performance
#structure of this code:
#load API [#] tags: manually write some, like the case in the paper, see All-api-signature.txt and all-raw data
#load tree: read tree in memory, 
###getAllTagsBasedOnLevel(tag1, level, direction) return tags in the tree based on the note and level (up, down or both)
#getChildTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level 
#getParentTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level 

#isComposibleByTag(tag1, tag2, tree level)  whether tag1 < tag2
#isComposibleByTagList(list1, list2, tree level)  whether exist tag1 in the list1, has any tag1< tag2 that in the list2
#isComposibleApi(api1, api2, tree level)  -> call isComposibleByTagList the list of input/output

#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each

#define expectedComposibleApiList [api1#]: api2#, api3# ...
#calculate R=C/(C+M) P=C/(C+I) F=2PR/(P+R)


import sys
import re
import tree

#read tree
inputfTree = 'tags-tree-140-1k-s.txt'
outputfTree = file('treeeeee.txt', 'w')

#read tree
#parent[] for the parent list, everytime reading a (n) number'-' and a note, do the following:
#1. add a child to the tree: parent note is parent[n-1], child note is note
#2. update parent[n] = note

INIT_TREE_NOTE_VALUE = 0

tagTree = tree.Tree()  #initial tree
parentList = {}

#load tree in to memory
def read_Tree(line):
	lineList = line.split(' ')
	if (len(lineList)==0):
		return
	if (len(lineList)==1):
		#add tree root
		tagTree.create_node(INIT_TREE_NOTE_VALUE, lineList[0]) 	
		parentList[0]=lineList[0].strip()
	if (len(lineList)==2):
		#add child note	
		level = len(lineList[0].strip())
		parantLevel = level - 1
		currentNote = lineList[1].strip()
		parantNote = parentList[parantLevel]
		tagTree.create_node(INIT_TREE_NOTE_VALUE, currentNote, parent = parantNote)
		parentList[level] = currentNote

with open(inputfTree) as f:
	for line in f:
		read_Tree(line) #parse the line through various functions

tagTree.show('treeRoot',outputfTree)
print "tree reading is done!"

#getChildTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level 
#getParentTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level

outputfTree.close()

#tagsList = tagTree.getChildTags('audio', 2)
#tagsList = tagTree.getParentTags('community', 2)
#print tagsList


#isComposibleByTag(tag1, tag2, tree level)  whether tag1 < tag2
#isComposibleByTagList(list1, list2, tree level)  whether exist tag1 in the list1, has any tag1< tag2 that in the list2


def isComposibleByTag(tag1, tag2, level):
	if tag1 == tag2:   #if equal, composible
		return 1
	else:
		tagsList = tagTree.getParentTags(tag1, level)
		if tag2 in tagsList:
			return 1
		else:
			return 0

def isComposibleByTagList(list1, list2, level):
	for tag1 in list1:
		for tag2 in list2:
			if isComposibleByTag(tag1, tag2, level):
				return 1
	return 0
		
#test composible
#print isComposibleByTag('mp3', 'audio', 2)
#list1 = ['a','mp3']
#list2 = ['audio','asdva']
#print isComposibleByTagList(list1, list2, 2)


#define API with example: three dimention dict
#ApiList = {
#1: { 
#{'M': ['tag1', 'tag1']}, {'I': ['tag1', 'tag1']}, {'O': ['tag1', 'tag1']}, {'U': ['tag1', 'tag1']}, {'D': ['tag1', 'tag1']} 
#}
#2: { 
#{'M': ['tag1', 'tag1']}, {'I': ['tag1', 'tag1']}, {'O': ['tag1', 'tag1']}, {'U': ['tag1', 'tag1']}, {'D': ['tag1', 'tag1']} 
#}
#}

#------ audio
#------- music
#-------- mp3

Api1 = {}
Api1['M'] = ['tm1', 'tm2']
Api1['I'] = ['ti1', 'ti2']
Api1['O'] = ['mp3', 'to2']
Api1['U'] = ['tu1', 'tu2']
Api1['D'] = ['td1', 'td2']

Api2 = {}
Api2['M'] = ['tm1', 'tm2']
Api2['I'] = ['mp3', 'ti2']
Api2['O'] = ['to1', 'to2']
Api2['U'] = ['tu1', 'tu2']
Api2['D'] = ['td1', 'td2']

Api3 = {}
Api3['M'] = ['tm1', 'tm2']
Api3['I'] = ['music', 'ti2']
Api3['O'] = ['music', 'to2']
Api3['U'] = ['tu1', 'tu2']
Api3['D'] = ['td1', 'td2']

ApiList = {}
ApiList[1]=Api1
ApiList[2]=Api2
ApiList[3]=Api3
for api in ApiList:
	print "%s" %api, ":", ApiList[api]

#isComposibleApi(api1, api2, tree level)  -> call isComposibleByTagList the list of input/output
def isComposibleApi(api1, api2, level):
	list1 = api1['O']
	list2 = api2['I']
	if(len(list1)>=0 and len(list2)>=0):
		return isComposibleByTagList(list1, list2, level)
	else:
		return 0
#print isComposibleApi(Api1, Api2, 2)


#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each
def findComposibleApisbyGivenApi(num_api_to_be_composed, api_to_be_composed, api_all, level):
	apiComposibleList = []
	for (k,v) in api_all.items():
		#if the api != api_to_be_composed
		if(k != num_api_to_be_composed):
			if (isComposibleApi(v, api_to_be_composed, level)): #find input of the current
				apiComposibleList.append(k)
			elif(isComposibleApi(api_to_be_composed, v, level)): #find output of the current
				apiComposibleList.append(k)
	return apiComposibleList
#print findComposibleApisbyGivenApi(Api2, ApiList, 2)

learntComposibleApis = {}
def findAllComposibleApis(api_all, level):
	for (k,v) in api_all.items():		
		learntComposibleApis[k] = findComposibleApisbyGivenApi(k, v, api_all, level)

findAllComposibleApis(ApiList, 2)		
print "learntComposibleApis: ", learntComposibleApis


#define expectedComposibleApiList [api1#]: api2#, api3# ...
#expectedComposibleApis
expectedComposibleApis = {1: [2,3], 2: [3,4], 4: [3]}
print "expectedComposibleApis: ", expectedComposibleApis

#calculate R=C/(C+M) P=C/(C+I) F=2PR/(P+R)
#C = correct (learnt U expected), M = missing (learnt - expected), I = incorrect (expected - learnt), 

CORRECT = 0
MISSING = 0
INCORRECT = 0
RECALL = 0.0
PRECISION = 0.0
F_MEASURE = 0.0

def calculatePerformance(expectedDict, learntDict):
	global CORRECT
	global MISSING
	global INCORRECT
	global RECALL
	global PRECISION
	global F_MEASURE
	
	for (ek,ev) in expectedDict.items():
		if(ek in learntDict.keys()):
			eSet = set(expectedDict[ek])
			lSet = set(learntDict[ek])
			CORRECT += len(eSet & lSet)
			MISSING += len(eSet - lSet)
			INCORRECT += len(lSet - eSet)
		else:  # not found in learnt, all missing
			eSet = set(expectedDict[ek])
			MISSING += len(eSet)
	for (ek,ev) in learntDict.items():  # not found in expected, all incorrect
		if(ek not in expectedDict.keys()): 
			eSet = set(learntDict[ek])
			INCORRECT += len(eSet)
			
	#calculate R=C/(C+M) P=C/(C+I) F=2PR/(P+R)
	if(CORRECT+MISSING>0):
		RECALL = (1.0*CORRECT)/(1.0*(CORRECT+MISSING))
	if(CORRECT+INCORRECT>0):
		PRECISION = (1.0*CORRECT)/(1.0*(CORRECT+INCORRECT))
	if(RECALL+PRECISION>0):
		F_MEASURE = (2.0*RECALL*PRECISION)/(RECALL+PRECISION)

calculatePerformance(expectedComposibleApis, learntComposibleApis)
print "CORRECT: ", "%d" %CORRECT
print "MISSING: ", "%d" %MISSING
print "INCORRECT: ", "%d" %INCORRECT
print "RECALL: ", "%3.4f" %RECALL
print "PRECISION: ", "%3.4f" %PRECISION
print "F_MEASURE: ", "%3.4f" %F_MEASURE

	
			
			
	
			
			










