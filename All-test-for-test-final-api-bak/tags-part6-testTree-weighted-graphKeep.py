#Nov 29: for all the tags in a branch, instead of only connected pairs
#how to: get notesSet from reading
#		 allGenerationList = {} for each note, has a list of parents(grandparents...)
#					how to: from the tree, get its generation
#	     then call the compare function with criteria and sum/avg

#Nov 29: not the apis numbers, but all the tags used, sum(tiNtj)/sum(tiUtj)


#Nov 28: test tree (100, 1k, 2k) itself, for every two notes connected on the tree, sum the following: 1) structural apis(tiNtj)/apis(tiUtj) 2) Syntactic: Level 3)Symantic: Wordnet synonym

#read tree first
#load APIs, get TagSet, get TagPairs
#calculate

import tree
#inputfTree = 'tags-tree-140-1k-s2.txt'
#outputfTest = file('tree-test-140-1k-s2-wed.txt', 'w')
inputfTree = 'tags-tree-10_3-dot3-s.txt'

outputfTest = file('tree-test-all-final-s-10_3-dot3.txt', 'w')

#APIs for reading
inputf = '$$all-api-signature.txt'
outputfTag = file('tags-tag-part6.txt', 'w')


#read tree
#parent[] for the parent list, everytime reading a (n) number'-' and a note, do the following:
#1. add a child to the tree: parent note is parent[n-1], child note is note
#2. update parent[n] = note

INIT_TREE_NOTE_VALUE = 0

tagTree = tree.Tree()  #initial tree
parentList = {} #for parsing, temporary

#allChildrenList = {} #for test1, each note has a list of children, only one geneartion
allGenerationList= {} # all ancestors of each note #tagsList = tagTree.getParentTags(tag1, level=20)

treeNoteSet = []


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
		#add to note set
		treeNoteSet.append(currentNote)		
		#for test1, all children (1 level down) of each note
		#if(parantNote not in allChildrenList.keys()):
		#	allChildrenList[parantNote] = []
		#allChildrenList[parantNote].append(currentNote) 
		parentList[level] = currentNote

with open(inputfTree) as f:
	for line in f:
		read_Tree(line) #parse the line through various functions

#tagTree.show('treeRoot',outputfTree)
#print "tree reading is done!"
#outputfTree.close()

treeNoteSet = set(treeNoteSet)
for note in treeNoteSet:
	allGenerationList[note] = []
	#allGenerationList[note] = tagTree.getParentTags(note, 2)
	allGenerationList[note] = tagTree.getParentTags(note)
	
#print allGenerationList
#print allChildrenList


#read the APIs


#parameters affect the performance
Duplicated_Tags_of_Signature = 1      # whether allowing api signature duplicated (1 allowable; 0 not allowable)
Threthold_Tag_Set = 10                # remove the single tag with lower frequency 
Threthold_Tag_Pair = 3               # if greater than this number, the edge is connected (1) of two tags, otherwise, unconnected (0)
# remove the tag pairs with lower frequency

RATIO_LEVENSHTEIN = 0.35              # Similarity_Syntactic; the higher, the more significant
SYNONYM_YES_RATIO = 1               # Similarity_Semantic, if they are; the lower, the more significant
SYNONYM_NO_RATIO = 0	              # Similarity_Semantic, if not; the lower, the more significant

MAXLINE = 0 	
myTagSet = {}
myAPITags = [[0 for col in range(MAXLINE)] for row in range(MAXLINE)]  #the 2nd imention is a dict


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
	if v < Threthold_Tag_Set:
		del myTagSet[k]
		tag_set_removed = tag_set_removed+1 

print "tagSet has been shorten!"+ "%d" %tag_set_removed 


print >> outputfTag, "[TagSet]:"
for (k,v) in myTagSet.items():
	print >> outputfTag, "%s:" %k, "%d" %v
	
outputfTag.close()


#do the test
#1: structural: apis(tiNtj)/apis(tiUtj); apis(tiNtj)/min(apis(ti),apis(tj)); apis(tiNtj)/max(apis(ti),apis(tj)) 
#2: Syntactic: Level
#3: Symantic: Wordnet synonym


def sumOfTagsHavingTags(tag1, tag2): 
	num_both = 0	
	for myAPI in myAPITags:
		if tag1 in myAPI.keys() and tag2 in myAPI.keys():	 #for any two in a line #myAPI[tag1]  #if tag_name in readinglist.keys():
			num_both+= min(myAPI[tag1], myAPI[tag2])		
	return num_both

	
def numberOfAPIsHavingTag(tag):
	num_taga = 0	
	for myAPI in myAPITags:
		if tag in myAPI.keys():	 #for any two in a line #myAPI[tag1]  #if tag_name in readinglist.keys():
			num_taga+=1			
	return num_taga

def numberOfAPIsHavingTags(tag1, tag2): 
	num_both = 0	
	for myAPI in myAPITags:
		if tag1 in myAPI.keys() and tag2 in myAPI.keys():	 #for any two in a line #myAPI[tag1]  #if tag_name in readinglist.keys():
			num_both+=1			
	return num_both
	
def structrualByUnion(tag1, tag2):
	num_both = numberOfAPIsHavingTags(tag1, tag2)
	num_tag1 = numberOfAPIsHavingTag(tag1)
	num_tag2 = numberOfAPIsHavingTag(tag2)
	return 1.0*num_both/(1.0*(num_tag1+num_tag2))
	
def structrualByMin(tag1, tag2):
	num_both = numberOfAPIsHavingTags(tag1, tag2)
	num_tag1 = numberOfAPIsHavingTag(tag1)
	num_tag2 = numberOfAPIsHavingTag(tag2)
	return 1.0*num_both/(1.0*(min(num_tag1,num_tag2)))
	
def structrualByMax(tag1, tag2):
	num_both = numberOfAPIsHavingTags(tag1, tag2)
	num_tag1 = numberOfAPIsHavingTag(tag1)
	num_tag2 = numberOfAPIsHavingTag(tag2)
	return 1.0*num_both/(1.0*(max(num_tag1,num_tag2)))

	
#test 2: Syntactic, levenshtein
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
            
    #return current[n]
	return current[n]/(1.0*max(n, m))
	
#test 3: 
import SynonymWordnet
def synonym(tag1, tag2):
	is_synonym = 0.0
	if (SynonymWordnet.check_synonym (tag2, tag1) == 1):
		is_synonym = SYNONYM_YES_RATIO
	else:
		is_synonym = SYNONYM_NO_RATIO
	return is_synonym
	
#test3: get the similarity semantic of two tags, use path similarity of wordnet
import PathSimilarity
def synonymSimilarity(tag1, tag2):
	return PathSimilarity.pathSimilarity(tag1, tag2)
	
STRUCTURAL_UNION = 0.0;
STRUCTURAL_MIN = 0.0;
STRUCTURAL_MAX = 0.0;
SYNTACTIC_LEVEN = 0.0;
SEMANTIC_SYNONYM = 0.0;
NUMBER_TESTPAIR = 0;
#Dec 1: for tree, the criteria above are not reflecting the tree (child and parent). the criteria is not always increasing, add the following ones, if child tags is greater than parant tags, it will decrease.
STRUCTURAL_UNION_SIGNED = 0.0;
STRUCTURAL_MIN_SIGNED = 0.0;
STRUCTURAL_MAX_SIGNED = 0.0; 
STRUCTURAL_COMMON_BY_DIFF_SIGNED = 0.0; # difference of the two
STRUCTURAL_DIFF_SIGNED = 0.0; 

#Dec 2: come on, assume tree t1(parent)->t2(child):  
STRUCTURAL_COMMON_SIGANED_CHILD = 0.0;  #((t1-t2)/|t1-t2|) * n(t1)N n(t2)/n(t2)
STRUCTURAL_COMMON_SIGANED_PARENT = 0.0;  #((t1-t2)/|t1-t2|) * n(t1)N n(t2)/n(t1)
STRUCTURAL_COMMON = 0.0 #just common sum
STRUCTURAL_COMMON_DIFF = 0.0 #common - diff
STRUCTURAL_COMMON_SIGNED = 0.0 #common +/- depends diff sign
	
#Nov 29, change from: not just connect notes, count all notes on a branch
def calculateTagPairInTree(list): # list is child -> parents
	global STRUCTURAL_UNION
	global STRUCTURAL_MIN	
	global STRUCTURAL_MAX
	global SYNTACTIC_LEVEN
	global SEMANTIC_SYNONYM
	global NUMBER_TESTPAIR
	#Added on Dec 1
	global STRUCTURAL_UNION_SIGNED
	global STRUCTURAL_MIN_SIGNED
	global STRUCTURAL_MAX_SIGNED
	global STRUCTURAL_COMMON_BY_DIFF_SIGNED
	global STRUCTURAL_DIFF_SIGNED
	global STRUCTURAL_COMMON_SIGANED_CHILD
	global STRUCTURAL_COMMON_SIGANED_PARENT
	
	global STRUCTURAL_COMMON
	global STRUCTURAL_COMMON_DIFF
	global STRUCTURAL_COMMON_SIGNED
	
	for (tag1,v) in list.items():
		for tag2 in v:
			if(tag1 != "treeRoot") and (tag2 != "treeRoot"):
				num_both = sumOfTagsHavingTags(tag1, tag2)
				num_tag1 = 0
				num_tag2 = 0
				if tag1 in myTagSet.keys(): 
					num_tag1 = myTagSet[tag1]
				if tag2 in myTagSet.keys(): 
					num_tag2 = myTagSet[tag2]
				
				#test1
				if(num_tag1 == 0 or num_tag2 == 0):
					s_union = 0
					s_min = 0
					s_max = 0
				else:
					s_union = 1.0*num_both/(1.0*(num_tag1+num_tag2))
					s_min = 1.0*num_both/(1.0*(min(num_tag1,num_tag2)))
					s_max = 1.0*num_both/(1.0*(max(num_tag1,num_tag2)))
				if (num_tag2-num_tag1 == 0 ): #parent - child
					s_diff = 0
					s_common_by_diff = 999
				else: 
					s_diff = num_tag2-num_tag1
					s_common_by_diff = 1.0*num_both/(1.0*(num_tag2-num_tag1))
				
				#test2
				leven = levenshtein(tag1, tag2)
				
				#test3
				#is_synonym = synonym(tag1, tag2)
				synonym_sim = synonymSimilarity(tag1, tag2)
				
				#print >> outputfTest, tag1, ": ", tag2, "s_union", "%3.2f" %s_union, "s_min", "%3.2f" %s_min,"s_max", "%3.2f" %s_max, "leven", "%3.2f" %leven, "synonym:", synonym_sim	
											
											
				STRUCTURAL_UNION +=  s_union
				STRUCTURAL_MIN +=  s_min
				STRUCTURAL_MAX +=  s_max
				SYNTACTIC_LEVEN += leven
				SEMANTIC_SYNONYM += synonym_sim
				NUMBER_TESTPAIR += 1
				
				STRUCTURAL_COMMON_BY_DIFF_SIGNED += s_common_by_diff
				STRUCTURAL_DIFF_SIGNED += s_diff
				
				if(num_tag1<=num_tag2): # expected, the child should has smaller number
					STRUCTURAL_UNION_SIGNED +=  s_union
					STRUCTURAL_MIN_SIGNED +=  s_min
					STRUCTURAL_MAX_SIGNED +=  s_max		
					if(num_tag1 != 0 and num_tag2 != 0):
						STRUCTURAL_COMMON_SIGANED_CHILD = STRUCTURAL_COMMON_SIGANED_CHILD + (1.0*num_both)/(1.0*num_tag1)
						STRUCTURAL_COMMON_SIGANED_PARENT = STRUCTURAL_COMMON_SIGANED_PARENT + (1.0*num_both)/(1.0*num_tag2)	

					STRUCTURAL_COMMON += num_both
					STRUCTURAL_COMMON_DIFF = STRUCTURAL_COMMON_DIFF + num_both + num_tag2 - num_tag1 #common - diff
					STRUCTURAL_COMMON_SIGNED = STRUCTURAL_COMMON_SIGNED + num_both #common +/- depends diff sign
				
				else: #bad, reduce the number
					STRUCTURAL_UNION_SIGNED =  STRUCTURAL_UNION_SIGNED - s_union
					STRUCTURAL_MIN_SIGNED =  STRUCTURAL_MIN_SIGNED - s_min
					STRUCTURAL_MAX_SIGNED =  STRUCTURAL_MAX_SIGNED - s_max			
					if(num_tag1 != 0 and num_tag2 != 0):					
						STRUCTURAL_COMMON_SIGANED_CHILD = STRUCTURAL_COMMON_SIGANED_CHILD - (1.0*num_both)/(1.0*num_tag1)
						STRUCTURAL_COMMON_SIGANED_PARENT = STRUCTURAL_COMMON_SIGANED_PARENT - (1.0*num_both)/(1.0*num_tag2)	
					
					STRUCTURAL_COMMON += num_both
					STRUCTURAL_COMMON_DIFF = STRUCTURAL_COMMON_DIFF + num_both + num_tag1 - num_tag2 #common - diff #common - diff
					STRUCTURAL_COMMON_SIGNED = STRUCTURAL_COMMON_SIGNED - num_both #common +/- depends diff sign
			
calculateTagPairInTree(allGenerationList)
			
print >> outputfTest, "$AVG_SYNTACTIC_LEVEN", "%3.5f" %(SYNTACTIC_LEVEN/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_SEMANTIC_SYNONYM", "%3.5f" %(SEMANTIC_SYNONYM/NUMBER_TESTPAIR)
print >> outputfTest, "$NUMBER_TESTPAIR", "%d" %(NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_UNION_SIGNED", "%3.5f" %(STRUCTURAL_UNION_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_MIN_SIGNED", "%3.5f" %(STRUCTURAL_MIN_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_MAX_SIGNED", "%3.5f" %(STRUCTURAL_MAX_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_COMMON_SIGNED", "%3.5f" %(STRUCTURAL_COMMON_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_COMMON_SIGANED_CHILD", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_CHILD/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_COMMON_SIGANED_PARENT", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_PARENT/NUMBER_TESTPAIR)	
		
print >> outputfTest, "\n\nAVG_STRUCTURAL_UNION", "%3.5f" %(STRUCTURAL_UNION/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_STRUCTURAL_MIN", "%3.5f" %(STRUCTURAL_MIN/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_STRUCTURAL_MAX", "%3.5f" %(STRUCTURAL_MAX/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_SYNTACTIC_LEVEN", "%3.5f" %(SYNTACTIC_LEVEN/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_SEMANTIC_SYNONYM", "%3.5f" %(SEMANTIC_SYNONYM/NUMBER_TESTPAIR)
print >> outputfTest, "NUMBER_TESTPAIR", "%d" %(NUMBER_TESTPAIR)

print >> outputfTest, "\nSTRUCTURAL_UNION", "%3.5f" %(STRUCTURAL_UNION)
print >> outputfTest, "STRUCTURAL_MIN", "%3.5f" %(STRUCTURAL_MIN)
print >> outputfTest, "STRUCTURAL_MAX", "%3.5f" %(STRUCTURAL_MAX)
print >> outputfTest, "SYNTACTIC_LEVEN", "%3.5f" %(SYNTACTIC_LEVEN)
print >> outputfTest, "SEMANTIC_SYNONYM", "%3.5f" %(SEMANTIC_SYNONYM)

print >> outputfTest, "\n$AVG_STRUCTURAL_UNION_SIGNED", "%3.5f" %(STRUCTURAL_UNION_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_MIN_SIGNED", "%3.5f" %(STRUCTURAL_MIN_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "$AVG_STRUCTURAL_MAX_SIGNED", "%3.5f" %(STRUCTURAL_MAX_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_STRUCTURAL_DIFF_SIGNED", "%3.5f" %(STRUCTURAL_DIFF_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_STRUCTURAL_COMMON_BY_DIFF_SIGNED", "%3.5f" %(STRUCTURAL_COMMON_BY_DIFF_SIGNED/NUMBER_TESTPAIR)

print >> outputfTest, "\nSTRUCTURAL_UNION_SIGNED", "%3.5f" %(STRUCTURAL_UNION_SIGNED)
print >> outputfTest, "STRUCTURAL_MIN_SIGNED", "%3.5f" %(STRUCTURAL_MIN_SIGNED)
print >> outputfTest, "STRUCTURAL_MAX_SIGNED", "%3.5f" %(STRUCTURAL_MAX_SIGNED)
print >> outputfTest, "STRUCTURAL_DIFF_SIGNED", "%3.5f" %(STRUCTURAL_DIFF_SIGNED)
print >> outputfTest, "STRUCTURAL_COMMON_BY_DIFF_SIGNED", "%3.5f" %(STRUCTURAL_COMMON_BY_DIFF_SIGNED)

print >> outputfTest, "\n$$AVG_STRUCTURAL_COMMON_SIGANED_CHILD", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_CHILD/NUMBER_TESTPAIR)
print >> outputfTest, "$$AVG_STRUCTURAL_COMMON_SIGANED_PARENT", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_PARENT/NUMBER_TESTPAIR)
print >> outputfTest, "STRUCTURAL_COMMON_SIGANED_CHILD", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_CHILD)
print >> outputfTest, "STRUCTURAL_COMMON_SIGANED_PARENT", "%3.5f" %(STRUCTURAL_COMMON_SIGANED_PARENT)

print >> outputfTest, "\nAVG_STRUCTURAL_COMMON", "%3.5f" %(STRUCTURAL_COMMON/NUMBER_TESTPAIR)
print >> outputfTest, "AVG_STRUCTURAL_COMMON_DIFF", "%3.5f" %(STRUCTURAL_COMMON_DIFF/NUMBER_TESTPAIR)
print >> outputfTest, "$$AVG_STRUCTURAL_COMMON_SIGNED", "%3.5f" %(STRUCTURAL_COMMON_SIGNED/NUMBER_TESTPAIR)
print >> outputfTest, "STRUCTURAL_COMMON", "%3.5f" %(STRUCTURAL_COMMON)
print >> outputfTest, "STRUCTURAL_COMMON_DIFF", "%3.5f" %(STRUCTURAL_COMMON_DIFF)
print >> outputfTest, "STRUCTURAL_COMMON_SIGNED", "%3.5f" %(STRUCTURAL_COMMON_SIGNED)

outputfTest.close()
print "DONE!"

	


