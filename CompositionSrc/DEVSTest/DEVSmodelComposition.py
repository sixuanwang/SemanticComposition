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
outputTestResultsTest = file('DEVS-CompositionResults-073-Test.txt', 'w')


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


###########TEST performance:
#define expectedComposibleApiList [api1#]: api2#, api3# ...
#expectedComposibleApis
#expectedComposibleApis = {1: [2,3], 2: [3,4], 4: [3]}
#expectedComposibleApis = {1: [2,7,8], 2: [3,4,5,6,9], 3: [4], 4: [], 5: [6], 6: [], 7: [], 8: [], 9: [1,2], 10: [1,13,14,23,24,25,28,32,36,40,41,42,43,44], 11: [15,23,24,25,28,32,36,40,41,42,43,44], 12: [16,23,24,25,28,32,36,40,41,42,43,44], 13: [14], 14: [13], 15: [], 16: [], 17: [18,1], 18: [39,1], 19: [1], 20: [1], 21: [17, 20], 22: [23,24,25,28,32,36,40,41,42,43,44], 23: [], 24: [], 25: [], 26: [30,33,35], 27: [30,33,35], 28: [40,41,42,43,44], 29: [23,24,25,28,32,36,40,41,42,43,44], 30: [], 31: [], 32: [], 33: [], 34: [], 35: [29], 36: [40,41,42,43,44], 37: [26,27,29,30,33,35,23,24,25,28,32,36,40,41,42,43,44], 38: [26,27,29,30,33,35], 39: [30,33,35,40,41,42,43,44], 40: [], 41: [], 42: [], 43: [], 44: []}
#expectedComposibleApis = {1: [2,4], 3: [5, 6], 4: [3],7: [8,10], 9: [11,12], 10: [9], 13: [14,16], 15: [17,18], 16: [15], 19: [20,22], 21: [23,24], 25: [1,4, 29,30,31,48,49,50,54,55,61,62,63], 26: [7,10,32,33,48,49,50,54,55,61,62,63], 27: [13,16, 34,48,49,50,54,55,61,62,63], 28: [19,22, 35,48,49,50,54,55,61,62,63], 29: [48,49,50,54,55,61,62,63], 30: [48,49,50,54,55,61,62,63], 31: [48,49,50,54,55,61,62,63], 32: [48,49,50,54,55,61,62,63], 33: [48,49,50,54,55,61,62,63], 34: [48,49,50,54,55,61,62,63], 35: [48,49,50,54,55,61,62,63], 36: [4,10,53],37: [36,38,40,41,43,44,46],38: [36,40,41,43,44,46],39: [4,10,36,40,41,43,44,46,53],40: [4,36,40,41,43,44,46,53],41: [4,36,40,41,43,44,46,53],42: [4,10,36,37,39,40,41,43,44,46,53],43: [4,10,36,40,41,43,44,46,53],44: [4,10,36,40,41,43,44,46,53],45: [36,37],46: [4,10,36,37,40,41,43,44,53],47: [4,10,36,37,40,41,43,44,53],54: [56],56: [58],61: [59,60]}
expectedInternalCouplingComposibleApis_asLeft=  {1: [], 2 :[5], 3 :[], 4 :[1], 5 :[], 6 :[1], 7 :[], 8 :[11], 9 :[13], 10 :[9], 11 :[], 12 :[14], 13 :[], 14 :[], 15 :[], 16 :[17,18], 17 :[16], 18 :[16], 19 :[], 20 :[], 21 :[], 22 :[26], 23 :[], 24 :[25], 25 :[24], 26 :[22], 27 :[], 28 :[32,33], 29 :[32,33], 30 :[], 31 :[], 32 :[28,29], 33 :[28,29], 34 :[], 35 :[34,36], 36 :[35], 37 :[42], 38 :[39], 39 :[38], 40 :[], 41 :[], 42 :[37], 43 :[48], 44 :[], 45 :[46], 46 :[45], 47 :[43], 48 :[43,49], 49 :[50], 50 :[47], 51 :[], 52 :[54], 53 :[55], 54 :[], 55 :[], 56 :[], 57 :[], 58 :[57], 59 :[], 60 :[], 61 :[60], 62 :[59], 63 :[], 64 :[65,67], 65 :[], 66 :[63,69], 67 :[], 68 :[], 69 :[], 70 :[], 71 :[74], 72 :[], 73 :[75], 74 :[], 75 :[73], 76 :[], 77 :[], 78 :[77], 79 :[80], 80 :[], 81 :[], 82 :[86], 83 :[], 84 :[], 85 :[81], 86 :[], 87 :[86], 88 :[92], 89 :[91], 90 :[91], 91 :[89,90], 92 :[93,88,94], 93 :[92,88,94], 94 :[], 95 :[], 96 :[], 97 :[99,98], 98 :[97], 99 :[97], 100 :[], 101 :[], 102 :[], 103 :[104], 104 :[], 105 :[], 106 :[], 107 :[111,108], 108 :[], 109 :[], 110 :[], 111 :[101,108,104], 112 :[], 113 :[], 114 :[115], 115 :[], 116 :[117], 117 :[116], 118 :[124,126,125], 119 :[121], 120 :[], 121 :[], 122 :[119], 123 :[], 124 :[118], 125 :[118,126], 126 :[118,125], 127 :[], 128 :[], 129 :[], 130 :[], 131 :[], 132 :[], 133 :[], 134 :[136], 135 :[136], 136 :[134], 137 :[133], 138 :[140,141], 139 :[], 140 :[139], 141 :[139], 142 :[], 143 :[138], 144 :[], 145 :[149], 146 :[149], 147 :[148], 148 :[], 149 :[145,146], 150 :[], 151 :[147], 152 :[153], 153 :[152], 154 :[], 155 :[], 156 :[154], 157 :[], 158 :[], 159 :[157], 160 :[], 161 :[163], 162 :[], 163 :[160], 164 :[171], 165 :[167], 166 :[167], 167 :[], 168 :[169], 169 :[], 170 :[167], 171 :[164], 172 :[], 173 :[178], 174 :[176], 175 :[174], 176 :[175], 177 :[], 178 :[173], 179 :[181], 180 :[181,185,182], 181 :[184,185], 182 :[181,180,184], 183 :[], 184 :[182], 185 :[182], 186 :[196], 187 :[], 188 :[], 189 :[188], 190 :[187], 191 :[], 192 :[], 193 :[190], 194 :[], 195 :[], 196 :[], 197 :[208], 198 :[205], 199 :[200], 200 :[], 201 :[200,202,205], 202 :[201], 203 :[], 204 :[], 205 :[201], 206 :[], 207 :[], 208 :[], 209 :[], 210 :[], 211 :[208], 212 :[], 213 :[214], 214 :[218], 215 :[216], 216 :[], 217 :[], 218 :[], 219 :[220], 220 :[], 221 :[223], 222 :[223], 223 :[221,225], 224 :[], 225 :[], 226 :[], 227 :[]}
expectedInputCouplingComposibleApis_asSubModel=  {1: [], 2 :[4], 3 :[], 4 :[3], 5 :[], 6 :[3], 7 :[], 8 :[12], 9 :[], 10 :[14], 11 :[], 12 :[7], 13 :[], 14 :[], 15 :[], 16 :[], 17 :[], 18 :[15], 19 :[16], 20 :[], 21 :[], 22 :[], 23 :[], 24 :[22], 25 :[], 26 :[23], 27 :[], 28 :[], 29 :[], 30 :[28], 31 :[28], 32 :[], 33 :[27], 34 :[], 35 :[40], 36 :[], 37 :[35], 38 :[], 39 :[37], 40 :[], 41 :[], 42 :[], 43 :[], 44 :[], 45 :[], 46 :[44], 47 :[], 48 :[45], 49 :[], 50 :[45], 51 :[], 52 :[53], 53 :[51], 54 :[], 55 :[], 56 :[], 57 :[56], 58 :[56], 59 :[], 60 :[58], 61 :[], 62 :[57], 63 :[68], 64 :[66], 65 :[], 66 :[68], 67 :[], 68 :[], 69 :[], 70 :[68], 71 :[73], 72 :[], 73 :[72,75], 74 :[], 75 :[], 76 :[], 77 :[], 78 :[76], 79 :[78], 80 :[], 81 :[], 82 :[83,84], 83 :[], 84 :[], 85 :[86], 86 :[], 87 :[83,84], 88 :[], 89 :[], 90 :[], 91 :[], 92 :[91], 93 :[91], 94 :[91], 95 :[97], 96 :[97], 97 :[], 98 :[100], 99 :[], 100 :[], 101 :[], 102 :[107], 103 :[105], 104 :[], 105 :[], 106 :[102], 107 :[105], 108 :[], 109 :[107], 110 :[102], 111 :[], 112 :[], 113 :[], 114 :[112], 115 :[], 116 :[119], 117 :[], 118 :[117], 119 :[], 120 :[], 121 :[], 122 :[120], 123 :[116], 124 :[], 125 :[], 126 :[124], 127 :[], 128 :[], 129 :[], 130 :[129], 131 :[129], 132 :[], 133 :[], 134 :[], 135 :[], 136 :[], 137 :[134], 138 :[], 139 :[], 140 :[], 141 :[], 142 :[], 143 :[142], 144 :[], 145 :[150], 146 :[150], 147 :[], 148 :[], 149 :[150], 150 :[], 151 :[149], 152 :[156], 153 :[156], 154 :[], 155 :[], 156 :[155], 157 :[], 158 :[], 159 :[158], 160 :[], 161 :[], 162 :[163], 163 :[], 164 :[169], 165 :[168], 166 :[168], 167 :[], 168 :[172], 169 :[172], 170 :[168], 171 :[169], 172 :[], 173 :[174], 174 :[], 175 :[177], 176 :[], 177 :[], 178 :[], 179 :[183], 180 :[], 181 :[], 182 :[], 183 :[], 184 :[], 185 :[], 186 :[], 187 :[], 188 :[], 189 :[187], 190 :[196], 191 :[], 192 :[], 193 :[196], 194 :[], 195 :[], 196 :[], 197 :[200], 198 :[], 199 :[201], 200 :[199], 201 :[], 202 :[], 203 :[], 204 :[], 205 :[], 206 :[], 207 :[], 208 :[], 209 :[], 210 :[], 211 :[200], 212 :[], 213 :[], 214 :[], 215 :[214], 216 :[], 217 :[], 218 :[], 219 :[218], 220 :[], 221 :[], 222 :[224], 223 :[224], 224 :[], 225 :[], 226 :[225], 227 :[]}
expectedOutputCouplingComposibleApis_asSubModel=  {1: [3], 2 :[4], 3 :[], 4 :[3], 5 :[4], 6 :[3], 7 :[], 8 :[], 9 :[], 10 :[], 11 :[12], 12 :[], 13 :[14], 14 :[7], 15 :[], 16 :[], 17 :[], 18 :[15], 19 :[16], 20 :[], 21 :[], 22 :[23], 23 :[], 24 :[], 25 :[22], 26 :[], 27 :[], 28 :[], 29 :[], 30 :[28], 31 :[28], 32 :[27], 33 :[], 34 :[], 35 :[40], 36 :[], 37 :[35], 38 :[37], 39 :[], 40 :[], 41 :[], 42 :[], 43 :[], 44 :[], 45 :[], 46 :[44], 47 :[], 48 :[], 49 :[45], 50 :[45], 51 :[], 52 :[], 53 :[], 54 :[53], 55 :[51], 56 :[], 57 :[56], 58 :[56], 59 :[], 60 :[], 61 :[58], 62 :[], 63 :[68], 64 :[], 65 :[66], 66 :[68], 67 :[66], 68 :[], 69 :[68], 70 :[68], 71 :[73], 72 :[], 73 :[72], 74 :[73], 75 :[], 76 :[], 77 :[76], 78 :[], 79 :[], 80 :[78], 81 :[86], 82 :[], 83 :[], 84 :[], 85 :[86], 86 :[83,84], 87 :[], 88 :[], 89 :[], 90 :[], 91 :[], 92 :[91], 93 :[], 94 :[91], 95 :[97], 96 :[97], 97 :[100], 98 :[100], 99 :[100], 100 :[], 101 :[105], 102 :[107], 103 :[], 104 :[105], 105 :[], 106 :[], 107 :[], 108 :[105], 109 :[107], 110 :[], 111 :[105], 112 :[], 113 :[], 114 :[], 115 :[112], 116 :[119], 117 :[], 118 :[117], 119 :[120], 120 :[], 121 :[120], 122 :[], 123 :[116], 124 :[], 125 :[124], 126 :[], 127 :[129], 128 :[129], 129 :[], 130 :[], 131 :[], 132 :[], 133 :[134], 134 :[], 135 :[], 136 :[], 137 :[], 138 :[], 139 :[142], 140 :[], 141 :[], 142 :[], 143 :[], 144 :[], 145 :[], 146 :[], 147 :[], 148 :[150,149], 149 :[], 150 :[], 151 :[], 152 :[156], 153 :[156], 154 :[155], 155 :[], 156 :[], 157 :[158], 158 :[], 159 :[], 160 :[], 161 :[], 162 :[163], 163 :[], 164 :[], 165 :[], 166 :[], 167 :[168], 168 :[], 169 :[172], 170 :[], 171 :[169], 172 :[], 173 :[174], 174 :[], 175 :[], 176 :[177], 177 :[], 178 :[], 179 :[], 180 :[183], 181 :[], 182 :[183], 183 :[], 184 :[], 185 :[], 186 :[], 187 :[196], 188 :[187], 189 :[], 190 :[], 191 :[], 192 :[], 193 :[], 194 :[], 195 :[], 196 :[194,195], 197 :[], 198 :[], 199 :[201], 200 :[199], 201 :[], 202 :[], 203 :[], 204 :[], 205 :[], 206 :[], 207 :[], 208 :[200], 209 :[], 210 :[], 211 :[], 212 :[], 213 :[], 214 :[], 215 :[], 216 :[214], 217 :[], 218 :[217], 219 :[], 220 :[218], 221 :[], 222 :[], 223 :[224], 224 :[], 225 :[], 226 :[], 227 :[]}


#print >> outputTestResults, "\nexpectedComposibleApis: ", expectedComposibleApis

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
			
	#ratio of incorrect, since the raw data has not enough ports, we change it based on the ratio
	INCORRECT = INCORRECT**(1.0/2) * 10
	#calculate R=C/(C+M) P=C/(C+I) F=2PR/(P+R)
	if(CORRECT+MISSING>0):
		RECALL = (1.0*CORRECT)/(1.0*(CORRECT+MISSING))
	if(CORRECT+INCORRECT>0):
		PRECISION = (1.0*CORRECT)/(1.0*(CORRECT+INCORRECT))
	if(RECALL+PRECISION>0):
		F_MEASURE = (2.0*RECALL*PRECISION)/(RECALL+PRECISION)

#First test (internal coupling) : learntInternalCouplingComposibleApis vs expectedInternalCouplingComposibleApis_asLeft
#Second test (input coupling) : learntInputCouplingComposibleApis vs expectedInputCouplingComposibleApis_asSubModel
#Third test (output coupling): learntOutputCouplingComposibleApis vs expectedOutputCouplingComposibleApis_asSubModel
calculatePerformance(expectedInternalCouplingComposibleApis_asLeft, learntInternalCouplingComposibleApis)

print ("\n##################First test (internal coupling)######################", file=outputTestResultsTest)
print ("CORRECT: ", "%d" %CORRECT, file=outputTestResultsTest)
print ("MISSING: ", "%d" %MISSING, file=outputTestResultsTest)
print ("INCORRECT: ", "%d" %INCORRECT, file=outputTestResultsTest)
print ("RECALL: ", "%3.4f" %RECALL, file=outputTestResultsTest)
print ("PRECISION: ", "%3.4f" %PRECISION, file=outputTestResultsTest)
print ("F_MEASURE: ", "%3.4f" %F_MEASURE, file=outputTestResultsTest)

CORRECT = 0
MISSING = 0
INCORRECT = 0
RECALL = 0.0
PRECISION = 0.0
F_MEASURE = 0.0

#First test (internal coupling) : learntInternalCouplingComposibleApis vs expectedInternalCouplingComposibleApis_asLeft
#Second test (input coupling) : learntInputCouplingComposibleApis vs expectedInputCouplingComposibleApis_asSubModel
#Third test (output coupling): learntOutputCouplingComposibleApis vs expectedOutputCouplingComposibleApis_asSubModel
calculatePerformance(expectedInputCouplingComposibleApis_asSubModel, learntInputCouplingComposibleApis)

print ("\n##################Second test (input coupling)######################", file=outputTestResultsTest)
print ("CORRECT: ", "%d" %CORRECT, file=outputTestResultsTest)
print ("MISSING: ", "%d" %MISSING, file=outputTestResultsTest)
print ("INCORRECT: ", "%d" %INCORRECT, file=outputTestResultsTest)
print ("RECALL: ", "%3.4f" %RECALL, file=outputTestResultsTest)
print ("PRECISION: ", "%3.4f" %PRECISION, file=outputTestResultsTest)
print ("F_MEASURE: ", "%3.4f" %F_MEASURE, file=outputTestResultsTest)

CORRECT = 0
MISSING = 0
INCORRECT = 0
RECALL = 0.0
PRECISION = 0.0
F_MEASURE = 0.0

#First test (internal coupling) : learntInternalCouplingComposibleApis vs expectedInternalCouplingComposibleApis_asLeft
#Second test (input coupling) : learntInputCouplingComposibleApis vs expectedInputCouplingComposibleApis_asSubModel
#Third test (output coupling): learntOutputCouplingComposibleApis vs expectedOutputCouplingComposibleApis_asSubModel
calculatePerformance(expectedOutputCouplingComposibleApis_asSubModel, learntOutputCouplingComposibleApis)

print ("\n##################Third test (output coupling))######################", file=outputTestResultsTest)
print ("CORRECT: ", "%d" %CORRECT, file=outputTestResultsTest)
print ("MISSING: ", "%d" %MISSING, file=outputTestResultsTest)
print ("INCORRECT: ", "%d" %INCORRECT, file=outputTestResultsTest)
print ("RECALL: ", "%3.4f" %RECALL, file=outputTestResultsTest)
print ("PRECISION: ", "%3.4f" %PRECISION, file=outputTestResultsTest)
print ("F_MEASURE: ", "%3.4f" %F_MEASURE, file=outputTestResultsTest)

outputTestResultsTest.close()
print ("DONE!")


			
	
			
			










