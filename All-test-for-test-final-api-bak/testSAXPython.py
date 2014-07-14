import xml.sax
 
class TagInfoHandler(xml.sax.ContentHandler):
	def __init__(self):
		xml.sax.ContentHandler.__init__(self)
		self.isDocument, self.isTag, self.isName, self.isWeight = 0, 0, 0, 0;
		self.toprint = ""
 
	def startElement(self, name, attrs):
		if name == "document":
			self.isDocument = 1
		if name == "tag":
			self.isTag = 1
		if name == "name":
			self.isName = 1
		if name == "weight":
			self.isWeight = 1
		
	def endElement(self, name):
		if name == "document":  #end of a resources, can output the line
			self.isDocument = 0
			self.toprint = self.toprint + "\n"
			outputfTag.write(self.toprint)
			self.toprint = ""
			self.isTag == 0
			self.isName == 0
			self.isWeight == 0 
		if name == "tag":
			self.isTag = 0
		if name == "name":
			self.isName = 0
		if name == "weight":
			self.isWeight = 0
 
	def characters(self, ch):		
		if self.isDocument == 1 and self.isTag == 1 and self.isName == 1:
			self.toprint = self.toprint + ch + ": "
		if self.isDocument == 1 and self.isTag == 1 and self.isWeight == 1:
			self.toprint = self.toprint + ch + " | "
			 
 
def main(sourceFileName):
		source = open(sourceFileName)
		xml.sax.parse(source, TagInfoHandler())
 
if __name__ == "__main__":
	outputfTag = open('tag140infor_parsed.txt', 'w') 
	main("taginfo.xml")	
	outputfTag.close()
	