#July 9, 2014:
# test DEVS models, find composible apis the data is collected from Model of List website, 
# < M | I | O >, I/O is a set of ports P,  each parameters has a set of tags AA, when matching should all tags of a parameter in the target, their should be a tag in a source has "<", not "any of"
# e.g. clock | time register | time_of_day  | time_set hour minute
# M = [clock time register] I = [[time of day]] O = [[time set] [hour] [minute]]

#structure of this code:
#load API [#] tags: manually got from DEVS models
#load tree: read tree in memory, 
#getChildTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level 
#getParentTags(tag1, level) return a lists of tags as the children of the given tag in the tree based on the note and level 

#isComposibleByTag(tag1, tag2, tree level)  whether tag1 < tag2
#isComposibleByTagList_Parameter_Strict(list1, list2, level))  whether exist tag1 in the list1, has all tags in list2 that tag1 <= tag2 
#isComposibleByTagList_Parameter_Loose(list1, list2, level))  whether exist tag1 in the list1, has any tag in list2 that tag1 <= tag2 

#isComposibleApi(api1, api2, tree level)  -> call isComposibleByTagList the list of input/output

#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each

from __future__ import print_function
import sys
import re
import tree

TREE_LEVEL_TO_BE_SEARCHED = 2 #Dec 10: configure how many levels to look up of the tree for finding the parents and children

inputApis = 'ExtractDEVSModelResults-NamePorts-selected-supposed-generated-v2 - manual tag.txt'
inputfTree = 'tags-tree-073.txt'
outputTestResults = file('DEVS-CompositionResults-073.txt', 'w')


#read API, now the API is a single line, only read I and O parameters, each parameter can have more than one tag
ApiList = {}
ApiCount = 1
def read_APIs(line):  
	global ApiCount
	lineList = line.split('|')
	if (len(lineList)!=4 ):
		return
	else:
		ApiRead  = {}
		ApiRead['M']=[]
		ApiRead['I']=[]
		ApiRead['O']=[]
		#add child note	  ApiRead['I'] ApiRead['O']	

		ApiRead['M'] = ApiRead['M'] + lineList[0].strip().split(' ') + lineList[1].strip().split(' ')
		
		
		readParameterList_I =lineList[3].strip().split(' ')  # each port
		
		for readParameter in readParameterList_I:
			readParameter = readParameter.strip()
			tagsInParameter_I = readParameter.split('_')   # each tag for port
			for elementInTags in tagsInParameter_I:
				if elementInTags.strip() == '':
					del elementInTags			
			ApiRead['I'].append(tagsInParameter_I)
		
		readParameterList_O = lineList[2].strip().split(' ') 
		
		for readParameter in readParameterList_O:
			tagsInParameter_O = readParameter.strip().split('_')
			for elementInTags in tagsInParameter_O:
				if elementInTags.strip() == '':
					del elementInTags
			ApiRead['O'].append(tagsInParameter_O)
		
		#ApiName = lineList[0].strip() + lineList[1].strip()
		
		ApiList[ApiCount] = ApiRead
		ApiCount += 1

with open(inputApis) as f:
	for line in f:
		read_APIs(line) #parse the line through various functions

#print I / O of reading
#for api in ApiList:
#	print(ApiList[api], file=outputTestResults)


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


def isComposibleByTag(tag1, tag2, level):
	if tag1 == tag2:   #if equal, composible
		return 1
	else:
		tagsList = tagTree.getParentTags(tag1, level)
		if tag2 in tagsList:
			return 1
		else:
			return 0

#for parameter, should all the tags of list2 be ">=" of list 1
def isComposibleByTagList_Parameter_Strict(list1, list2, level):
	flag = 0
	for tag2 in list2:		
		for tag1 in list1:
			if isComposibleByTag(tag1, tag2, level):
				flag = flag + 1
				break
				
	if flag == len(list2): # tag1 is not OK, not "child" of any one of list2
		return 1
	else:
		return 0
	
#for parameter, any tag of list2 be ">=" of list 1
def isComposibleByTagList_Parameter_Loose(list1, list2, level):
	flag = 0
	for tag2 in list2:		
		for tag1 in list1:
			if isComposibleByTag(tag1, tag2, level):
				flag = 1
				break
	if flag == 0: # tag1 is not OK, not "child" of any one of list2
		return 0
	return 1

#for API, if any (1 or more) parameter list of list2 has ">=" with any of the other, it is OK, note here we use _Strict (can be changed to _Loose)
def isComposibleByTagList_ParameterList(list1, list2, level):
		
	for taglist1 in list1:
		for taglist2 in list2:
			if isComposibleByTagList_Parameter_Strict(taglist1, taglist2, level):
				return 1
	return 0
		
		
#for API, get all composible lists of two lists, note here we use _Strict (can be changed to _Loose)
def getComposibleByTagList_ParameterList(list1, list2, level):
	composibleLists = []
	for taglist1 in list1:
		for taglist2 in list2:
			if isComposibleByTagList_Parameter_Strict(taglist1, taglist2, level):
				itemList = []
				itemList.append(taglist1)
				itemList.append('->')
				itemList.append(taglist2)
				composibleLists.append (itemList)
	return composibleLists
	

#isComposibleApi(api1, api2, tree level)  -> call isComposibleByTagList the list of input/output
#the internal coupling, api1's output links to api2's input
def isComposibleApiInternalCoupling(api1, api2, level):
	list1 = api1['O']
	list2 = api2['I']
	if(len(list2) == 0): #input is empty, so any list can be linked with it
		return 1
	if(len(list1)>=0 and len(list2)>=0):
		return isComposibleByTagList_ParameterList(list1, list2, level)
	else:
		return 0
#print isComposibleApi(Api1, Api2, 2)

#the input coupling, api1's input (atomic) links to api2's input (coupled)
def isComposibleApiInputCoupling(api1, api2, level):
	list1 = api1['I']
	list2 = api2['I']
	if(len(list2) == 0): #input is empty, so any list can be linked with it
		return 1
	if(len(list1)>=0 and len(list2)>=0):
		return isComposibleByTagList_ParameterList(list2, list1, level)
	else:
		return 0
		
#the output coupling, api1's output (atomic) links to api2's output (coupled), note the direction, actually api2 links to api1
def isComposibleApiOutputCoupling(api1, api2, level):
	list1 = api1['O']
	list2 = api2['O']
	if(len(list2) == 0): #input is empty, so any list can be linked with it
		return 1
	if(len(list1)>=0 and len(list2)>=0):
		return isComposibleByTagList_ParameterList(list1, list2, level)
	else:
		return 0

def getComposibleApi(api1, api2, level):
	list1 = api1['O']
	list2 = api2['I']	
	return getComposibleByTagList_ParameterList(list1, list2, level)
	
#print isComposibleApi(Api1, Api2, 2)


#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each
def findComposibleInternalCouplingbyGivenApi(num_api_to_be_composed, api_to_be_composed, api_all, level):
	apiComposibleList = []
	for (k,v) in api_all.items():
		#if the api != api_to_be_composed
		if(k != num_api_to_be_composed):
			if(isComposibleApiInternalCoupling(api_to_be_composed, v, level)): #find output of the current
				apiComposibleList.append(k)  ##return the API number
				#apiComposibleList.append(getComposibleApi(api_to_be_composed, v, level))   ##return the tag signature
			#elif (isComposibleApi(v, api_to_be_composed, level)): #find input of the current
			#	apiComposibleList.append(k)
	return apiComposibleList
#print findComposibleApisbyGivenApi(Api2, ApiList, 2)

#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each
def findComposibleInputCouplingbyGivenApi(num_api_to_be_composed, api_to_be_composed, api_all, level):
	apiComposibleList = []
	for (k,v) in api_all.items():
		#if the api != api_to_be_composed
		if(k != num_api_to_be_composed):
			if(isComposibleApiInputCoupling(api_to_be_composed, v, level)): #find output of the current
				apiComposibleList.append(k)  ##return the API number
				#apiComposibleList.append(getComposibleApi(api_to_be_composed, v, level))   ##return the tag signature
			#elif (isComposibleApi(v, api_to_be_composed, level)): #find input of the current
			#	apiComposibleList.append(k)
	return apiComposibleList
	
#findComposibleApis(api1, tree level)  -> return apiList [#], level is how deep we can find,+/-2, call isComposible for each
def findComposibleOutputCouplingbyGivenApi(num_api_to_be_composed, api_to_be_composed, api_all, level):
	apiComposibleList = []
	for (k,v) in api_all.items():
		#if the api != api_to_be_composed
		if(k != num_api_to_be_composed):
			if(isComposibleApiOutputCoupling(api_to_be_composed, v, level)): #find output of the current
				apiComposibleList.append(k)  ##return the API number
				#apiComposibleList.append(getComposibleApi(api_to_be_composed, v, level))   ##return the tag signature
			#elif (isComposibleApi(v, api_to_be_composed, level)): #find input of the current
			#	apiComposibleList.append(k)
	return apiComposibleList

learntInternalCouplingComposibleApis = {}
learntInputCouplingComposibleApis = {}
learntOutputCouplingComposibleApis = {}
def findAllComposibleApis(api_all, level):
	for (k,v) in api_all.items():		
		learntInternalCouplingComposibleApis[k] = findComposibleInternalCouplingbyGivenApi(k, v, api_all, level)
		learntInputCouplingComposibleApis[k] = findComposibleInputCouplingbyGivenApi(k, v, api_all, level)
		learntOutputCouplingComposibleApis[k] = findComposibleOutputCouplingbyGivenApi(k, v, api_all, level)

#HERE IS MAIN FUNCTION, ApiList is all what to test		
findAllComposibleApis(ApiList, TREE_LEVEL_TO_BE_SEARCHED)	

#for(composibleElement in learntComposibleApis):
	
print ("learntInternalCouplingComposibleApis(as left): ", learntInternalCouplingComposibleApis, file=outputTestResults)
print ("learntInputCouplingComposibleApis(as sub-model): ", learntInputCouplingComposibleApis, file=outputTestResults)
print ("learntOutputCouplingComposibleApis(as sub-model): ", learntOutputCouplingComposibleApis, file=outputTestResults)

outputTestResults.close()
print ("DONE!")
	
			
			
	
			
			










