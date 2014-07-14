import uuid
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

class Item:
	def __init__(self, name = "", type = "", description = ""):
		self.name = name   
		self.type = type    
		self.description = description 
		
def sanitize_id(id):
	return id.strip().replace(" ", "")

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Node:
	def __init__(self, name, identifier=None, expanded=True):
		self.__identifier = (str(uuid.uuid1()) if identifier is None else
				sanitize_id(str(identifier)))
		self.name = name
		self.expanded = expanded
		self.__bpointer = None
		self.__fpointer = []

	@property
	def identifier(self): # itself
		return self.__identifier

	@property
	def bpointer(self):   # parent
		return self.__bpointer

	@bpointer.setter      
	def bpointer(self, value):
		if value is not None:
			self.__bpointer = sanitize_id(value)

	@property
	def fpointer(self):   # child
		return self.__fpointer

	def update_fpointer(self, identifier, mode=_ADD):
		if mode is _ADD:
			self.__fpointer.append(sanitize_id(identifier))
		elif mode is _DELETE:
			self.__fpointer.remove(sanitize_id(identifier))
		elif mode is _INSERT:
			self.__fpointer = [sanitize_id(identifier)]

class Tree:		
	def __init__(self):
		self.nodes = []  # all the notes in the tree
		self.tagList = [] # used in the tag parents
		self.root = '' # the root of the tree
		self.item = None # the item for saveiing tree name, type and description
		self.INIT_TREE_NOTE_VALUE = 0

	def get_index(self, position):
		for index, node in enumerate(self.nodes):
			if node.identifier == position:
				break
		return index

	def create_node(self, name, identifier=None, parent=None):

		node = Node(name, identifier)
		self.nodes.append(node)
		self.__update_fpointer(parent, node.identifier, _ADD)
		node.bpointer = parent
		return node

	def saveTreeToXML(self, outputfilename):
		#save tree item: name, type, description
		tagTree = Element('TagTree')
		if(self.item):
			treeItem = SubElement(tagTree, 'Tree', name=str(self.item.name), type=str(self.item.type), description=str(self.item.description))
		
		#loop save each item
		self.saveTreeToXMLLoop(self.root, tagTree)
		
		#save the title and close
		outputf = open(outputfilename, 'w')
		outputf.write('<?xml version = "1.0"?>')
		outputf.write(ElementTree.tostring(tagTree))
		outputf.close()
		
	def saveTreeToXMLLoop(self, position, tagTree, level=_ROOT):
		queue = self[position].fpointer
		if (level == _ROOT):
			tagItem = SubElement(tagTree, 'Tag', name=self[position].identifier, index=str(0))
		else:
			indextemp = level
			tagItem = SubElement(tagTree, 'Tag', name=self[position].identifier, index=str(indextemp))
		if self[position].expanded:
			level += 1
			for element in queue:
				self.saveTreeToXMLLoop(element, tagTree, level)  # recursive call	
		
	def loadTreeFromXML(self, inputf):	
		document = ElementTree.parse(inputf)
			
		tree_name = document.find('Tree').attrib['name']
		tree_type = document.find('Tree').attrib['type']
		tree_description = document.find('Tree').attrib['description']
		treeItem = Item(tree_name, tree_type, tree_description)
		self.item = treeItem
					
		tagLines = document.findall('Tag')
		parentList = {}  #save parents so far
		
		for tagLine in tagLines: 
			tag_name = tagLine.attrib['name'].strip()
			tag_index = tagLine.attrib['index'].strip()
			if(tag_index == '0'): #root
				self.create_node(self.INIT_TREE_NOTE_VALUE, tag_name) 	
				parentList[0]= tag_name
				self.root = tag_name				
			else:  			#add child note					
				parantLevel = int(tag_index) - 1
				currentNote = tag_name
				parantNote = parentList[parantLevel]				
				self.create_node(self.INIT_TREE_NOTE_VALUE, currentNote, parent = parantNote)
				parentList[int(tag_index)] = currentNote
		
	#saveTree2File, previously is "show", save the tree to outputf
	def saveTreeToFile(self, outputfilename):
		outputf = file(outputfilename, 'w')
		self.saveTreeToFileLoop(self.root, outputf)
		outputf.close()
	
	def saveTreeToFileLoop(self, position, outputf, level=_ROOT):
		queue = self[position].fpointer
		if (level == _ROOT):
			print >> outputf, self[position].identifier
		else:
			print >> outputf, "-"*level, self[position].identifier
		if self[position].expanded:
			level += 1
			for element in queue:
				self.saveTreeToFileLoop(element, outputf, level)  # recursive call
	
	
	#loadTreeFromFile, previously in composition file
	def loadTreeFromFile(self, inputf):
		parentList = {}
		with open(inputf) as f:
			for line in f:
				lineList = line.split(' ')
				if (len(lineList)==0):
					continue
				if (len(lineList)==1):
					#add tree root
					self.create_node(self.INIT_TREE_NOTE_VALUE, lineList[0]) 	
					parentList[0]=lineList[0].strip()
					self.root = lineList[0].strip()
				if (len(lineList)==2):
					#add child note	
					level = len(lineList[0].strip())
					parantLevel = level - 1
					currentNote = lineList[1].strip()
					parantNote = parentList[parantLevel]
					self.create_node(self.INIT_TREE_NOTE_VALUE, currentNote, parent = parantNote)
					parentList[level] = currentNote
							
	#sixuan: get child tags based on the current 
	def getChildTagsRecursive(self, position, level, levelsToRead):
		queue = self[position].fpointer
		level += 1
		for element in queue:
			self.tagList.append(element)					
			if(level <= levelsToRead):
				self.getChildTagsRecursive(element, level, levelsToRead)

	def getChildTags(self, position, levelsToRead):
		self.tagList = []
		self.getChildTagsRecursive(position, 1, levelsToRead)
		return self.tagList	

	#sixuan: get child tags based on the current 
	def getParentTagsRecursive(self, position, level, levelsToRead):
		parent = self[position].bpointer		
		if (parent is not None): 
			self.tagList.append(parent)
			level += 1				
			if(level <= levelsToRead):
				self.getParentTagsRecursive(parent, level, levelsToRead)

	def getParentTags(self, position, levelsToRead=20):
		self.tagList = []
		self.getParentTagsRecursive(position, 1, levelsToRead)
		return self.tagList			
				
	def expand_tree(self, position, mode=_DEPTH):
		# Python generator. Loosly based on an algorithm from 'Essential LISP' by
		# John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
		yield position
		queue = self[position].fpointer
		while queue:
			yield queue[0]
			expansion = self[queue[0]].fpointer
			if mode is _DEPTH:
				queue = expansion + queue[1:]  # depth-first
			elif mode is _WIDTH:
				queue = queue[1:] + expansion  # width-first

	def is_branch(self, position):
		return self[position].fpointer

	def __update_fpointer(self, position, identifier, mode):
		if position is None:
			return
		else:
			self[position].update_fpointer(identifier, mode)

	def __update_bpointer(self, position, identifier):
		self[position].bpointer = identifier

	def __getitem__(self, key):
		return self.nodes[self.get_index(key)]

	def __setitem__(self, key, item):
		self.nodes[self.get_index(key)] = item

	def __len__(self):
		return len(self.nodes)

	def __contains__(self, identifier):
		return [node.identifier for node in self.nodes
				if node.identifier is identifier]

class TreeList:	
	def __init__(self, mdlist = {}):
		self.tagTreeList = mdlist ### dict: {'1': signature1, '2':signature2}
		self.totid = 0  	
		
	def saveTreeListToXML(self, outputfilename):
		tagTreeList = Element('TagTreeList')
		for tid,ts in self.tagTreeList.items():  ### for all valus in dict 
			tagTree = SubElement(tagTreeList, 'TagTree', id=str(tid)) 
	
			#save tree item: name, type, description
			if(ts.item):
				treeItem = SubElement(tagTree, 'Tree', name=str(ts.item.name), type=str(ts.item.type), description=str(ts.item.description))
			
			#loop save each item
			ts.saveTreeToXMLLoop(ts.root, tagTree)
		
		#save the title and close
		outputf = open(outputfilename, 'w')
		outputf.write('<?xml version = "1.0"?>')
		outputf.write(ElementTree.tostring(tagTreeList))
		outputf.close()
		
		
	def loadTreeListFromXML(self, inputf):	
		document = ElementTree.parse(inputf)
					
		for ts in document.findall('TagTree'):		
			tagTree = Tree()  ##to be saved
			
			tree_name = ts.find('Tree').attrib['name']
			tree_type = ts.find('Tree').attrib['type']
			tree_description = ts.find('Tree').attrib['description']
			treeItem = Item(tree_name, tree_type, tree_description)	
			tagTree.item = treeItem
					
			tagLines = ts.findall('Tag')
			parentList = {}  #save parents so far
			
			for tagLine in tagLines: 
				tag_name = tagLine.attrib['name'].strip()
				tag_index = tagLine.attrib['index'].strip()
				if(tag_index == '0'): #root
					tagTree.create_node(tagTree.INIT_TREE_NOTE_VALUE, tag_name) 	
					parentList[0]= tag_name
					tagTree.root = tag_name				
				else:  			#add child note					
					parantLevel = int(tag_index) - 1
					currentNote = tag_name
					parantNote = parentList[parantLevel]				
					tagTree.create_node(tagTree.INIT_TREE_NOTE_VALUE, currentNote, parent = parantNote)
					parentList[int(tag_index)] = currentNote
					
			self.tagTreeList[ts.attrib['id']] = tagTree 
			tagTree = None			
		
		
if __name__ == "__main__":
	treeList = TreeList()
	treeList.loadTreeListFromXML("treelist-in.xml")
	treeList.saveTreeListToXML("treelist-out.xml")
	
