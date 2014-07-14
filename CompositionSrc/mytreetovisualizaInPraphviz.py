#Mar 17: to read tree  and generate the graphviz

import tree
inputfTree = 'test-for-visual-api.txt'
outputfTest = file('graphviz-test-for-visual-api.txt', 'w')

#read tree
#parent[] for the parent list, everytime reading a (n) number'-' and a note, do the following:
#1. add a child to the tree: parent note is parent[n-1], child note is note
#2. update parent[n] = note

INIT_TREE_NOTE_VALUE = 0

tagTree = tree.Tree()  #initial tree
parentList = {} #for parsing, temporary


print >> outputfTest, "digraph unix {"
print >> outputfTest, "    size=\"200,200\";"
print >> outputfTest, "    node [color=lightblue2, style=filled];"


#load tree in to memory
def read_Tree(line):
	lineList = line.split(' ')
	if (len(lineList)==0):
		return
	if (len(lineList)==1):
		#add tree root
		#tagTree.create_node(INIT_TREE_NOTE_VALUE, lineList[0]) 	
		parentList[0]=lineList[0].strip()
	if (len(lineList)==2):
		#add child note	
		level = len(lineList[0].strip())
		parantLevel = level - 1
		currentNote = lineList[1].strip()
		parantNote = parentList[parantLevel]
		#tagTree.create_node(INIT_TREE_NOTE_VALUE, currentNote, parent = parantNote)
		print >> outputfTest, "    \"",parantNote.strip(),"\" -> \"", currentNote.strip(), "\";"
		#for test1, all children (1 level down) of each note
		#if(parantNote not in allChildrenList.keys()):
		#	allChildrenList[parantNote] = []
		#allChildrenList[parantNote].append(currentNote) 
		parentList[level] = currentNote

with open(inputfTree) as f:
	for line in f:
		read_Tree(line) #parse the line through various functions

print >> outputfTest, "\n}"
#tagTree.show('treeRoot',outputfTree)
#print "tree reading is done!"
#outputfTree.close()

