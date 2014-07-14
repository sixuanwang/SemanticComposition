""" Author: Peiwen Chen 
    Date: July 10th, 2014"""



from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

class Port:
    def __init__(self, pname = [], ptype = [], description = []):
	self.PortName = pname   
	self.Type = ptype    
	self.Description = description 
	


class TagSignature:
    def __init__(self, tagtype=None, nametag = [""], inputports = [], outputports = []):
        " self.* are the values stored in xml "
	self.tagtype = tagtype
	self.nametag = nametag  
	self.inputPorts = inputports 
	self.outputPorts = outputports 

    def loadTagSignatureFromXML(self, xmldir):
	document = ElementTree.parse(xmldir)

	self.tagtype = document.find('TagType').text
	self.nametag = document.find('NameTag').text
	
	inputs = document.find('Inputs')  
	for port in inputs.findall('Port'): 
	    ### create a new Port 
            newport = Port(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
	    self.inputPorts.append(newport) 
	
	outputs = document.find('Outputs')
	for port in outputs.findall('Port'):
	     port2add = Port(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
	     self.outputPorts.append(port2add)

    def saveTagSignatureToXML(self, xmldir):
	tagsignature = Element('TagSignature')
	tagtype = SubElement(tagsignature, 'TagType')  
	tagtype.text = str(self.tagtype)  
	nametag = SubElement(tagsignature, 'NameTag')
	nametag.text = str(self.nametag)   
	
	### Inputs Ports
	inputs = SubElement(tagsignature, 'Inputs')
	for port in self.inputPorts: ### for each port in the inputs Port List
	    inputport = SubElement(inputs, 'Port')  
	    inputportname = SubElement(inputport, 'PortName')
	    inputportname.text = str(port.PortName) ###add PortName value
	    inputporttype = SubElement(inputport, 'Type')
	    inputporttype.text = str(port.Type) ###add Type value
	    inputportdes = SubElement(inputport, 'Description')
	    inputportdes.text = str(port.Description) ###add des value
	
	### Outputs Ports
	outputs = SubElement(tagsignature, 'Outputs')
	for port in self.outputPorts: ### for each port in the inputs Port List
	    outputport = SubElement(outputs, 'Port')  
	    outputportname = SubElement(outputport, 'PortName')
	    outputportname.text = str(port.PortName) ###add PortName value
	    outputporttype = SubElement(outputport, 'Type')
	    outputporttype.text = str(port.Type) ###add Type value
	    outputportdes = SubElement(outputport, 'Description')
	    outputportdes.text = str(port.Description) ###add des value
	
	###write into xml file
	output_file = open(xmldir, 'w')
	output_file.write('<?xml version = "1.0"?>')
	output_file.write(ElementTree.tostring(tagsignature))
	output_file.close()



class TagSignatureList:
    "list of TagSignature"
    def __init__(self, tslist = {}):
	self.tagSignatureList = tslist ### dict: {'1': signature1, '2':signature2}
	self.totid = 0  

    def loadTagSignatureListFromXML(self, xmldir):
	tslistdoc = ElementTree.parse(xmldir)
	for ts in tslistdoc.findall('TagSignature'):
            newts = TagSignature() ### create a new TagSignature
	    newts.tagtype = ts.find('TagType').text
	    newts.nametag = ts.find('NameTag').text
	
	    inputs = ts.find('Inputs')  
	    for port in inputs.findall('Port'):  
                port2add = Port(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
	        newts.inputPorts.append(port2add) 
	
	    outputs = ts.find('Outputs')
	    for port in outputs.findall('Port'):
	         port2add = Port(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
	         newts.outputPorts.append(port2add) 
	
	    self.tagSignatureList[self.totid] =newts  ###add new signature to the dictory, id is totid
	    self.totid += 1


    def saveTagSignatureListToXML(self, xmldir):	
	tslist = Element('TagSignatureList')
        for ts in self.tagSignatureList.values():  ### for all valus in dict 
            tss = SubElement(tslist, 'TagSignature') ### create a new TagSignature Node

	    tagtype = SubElement(tss, 'TagType') 
	    tagtype.text = str(ts.tagtype)  
	    nametag = SubElement(tss, 'NameTag')
	    nametag.text = str(ts.nametag)   
	
	    ### Inputs Ports
	    inputs = SubElement(tss, 'Inputs')
	    for port in ts.inputPorts: 
	        inputport = SubElement(inputs, 'Port') ###create a new Port 
	        inputportname = SubElement(inputport, 'PortName')
	        inputportname.text = str(port.PortName)
	        inputporttype = SubElement(inputport, 'Type')
	        inputporttype.text = str(port.Type)
	        inputportdes = SubElement(inputport, 'Description')
	        inputportdes.text = str(port.Description) 
	
	    ### Outputs Ports
	    outputs = SubElement(tss, 'Outputs')
	    for port in ts.outputPorts: 
	        outputport = SubElement(outputs, 'Port')  
	        outputportname = SubElement(outputport, 'PortName')
	        outputportname.text = str(port.PortName) 
	        outputporttype = SubElement(outputport, 'Type')
	        outputporttype.text = str(port.Type)
	        outputportdes = SubElement(outputport, 'Description')
	        outputportdes.text = str(port.Description) 
	
	###write into xml file
	output_file = open(xmldir, 'w')
	output_file.write('<?xml version = "1.0"?>')
	output_file.write(ElementTree.tostring(tslist))
	output_file.close()






print "-----------I am doing test class TagSignature----------------\n"

tagsi = TagSignature('0')
tagsi.loadTagSignatureFromXML('config.xml')
tagsi.saveTagSignatureToXML('writeconfig.xml')


print "-------------I am doing test class TagSignatureList! ---------\n"
tagsilist = TagSignatureList()
tagsilist.loadTagSignatureListFromXML('configlist.xml')
tagsilist.saveTagSignatureListToXML('writeconfiglist.xml')
