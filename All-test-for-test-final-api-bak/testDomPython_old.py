import sys
import xml.dom.minidom

inputf = file('taginfo.xml')
outputfTag = open('tag140infor_parsed.txt', 'w')



dom = xml.dom.minidom.parse(inputf)

def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

def handleDataset(dom):
	documents = dom.getElementsByTagName("document")
	handleDocuments(documents)

def handleDocuments(documents):
	for document in documents:
		handleDocument(document)
		outputfTag.write("\n")
		
def handleDocument(document):
	tags = document.getElementsByTagName("tag")
	handleTags(tags)
	
def handleTags(tags):
	for tag in tags:
		handleTag(tag)
		
def handleTag(tag):
	name = tag.getElementsByTagName("name")[0]
	count = tag.getElementsByTagName("weight")[0]
	toprint = getText(name.childNodes) + ": " + getText(count.childNodes) + " | "
	outputfTag.write(toprint)
	
handleDataset(dom)

outputfTag.close()