import uuid

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
	def bpointer(self):   # parent?
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
		self.nodes = []
		self.tagList = []

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

	def show(self, position, outputf, level=_ROOT):
		queue = self[position].fpointer
		if (level == _ROOT):
			print >> outputf, self[position].identifier
		else:
			print >> outputf, "-"*level, self[position].identifier
		if self[position].expanded:
			level += 1
			for element in queue:
				self.show(element, outputf, level)  # recursive call
				
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

if __name__ == "__main__":

	tree = Tree()
	tree.create_node("Harry", "harry")  # root node
	tree.create_node("Jane", "jane", parent = "harry")
	tree.create_node("Bill", "bill", parent = "harry")
	tree.create_node("Joe", "joe", parent = "jane")
	tree.create_node("Diane", "diane", parent = "jane")
	tree.create_node("George", "george", parent = "diane")
	tree.create_node("Mary", "mary", parent = "diane")
	tree.create_node("Jill", "jill", parent = "george")
	tree.create_node("Carol", "carol", parent = "jill")
	tree.create_node("Grace", "grace", parent = "bill")
	tree.create_node("Mark", "mark", parent = "jane")

	outputf2 = file('tags-tree-teeeeest.txt', 'w')
	tree.show('harry',outputf2)
	outputf2.close()
	
'''
    print("="*80)
    tree.show("harry")
    print("="*80)
    for node in tree.expand_tree("harry", mode=_WIDTH):
        print(node)
    print("="*80)
'''