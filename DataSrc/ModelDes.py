
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

#parameter is used in model name and input/output parameters
class Item:
    def __init__(self, name = "", type = "", description = ""):
	self.name = name   
	self.type = type    
	self.description = description 
	
#model description has Model Item, inputs/outputs port items, and file items, each has name, type, and description
class ModelDescription:
    def __init__(self, model=None, inputports = [], outputports = [], files = []):
        " self.* are the values stored in xml "
	self.model = model
	self.inputPorts = inputports
	self.outputPorts = outputports
	self.files = files

    def loadModelDescriptionFromXML(self, xmldir):
		document = ElementTree.parse(xmldir)
		
		model_name = document.find('Model').attrib['name']
		model_type = document.find('Model').attrib['type']
		model_description = document.find('Model').attrib['description']
		modelItem = Item(model_name, model_type, model_description)
		self.model = modelItem
		
		print model_name, model_type
		
		inputs = document.find('Inputs')  
		for port in inputs.findall('Port'): 
			### create a new Port 
			newport = Item(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
			self.inputPorts.append(newport) 
		
		outputs = document.find('Outputs')
		for port in outputs.findall('Port'):
			 port2add = Item(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
			 self.outputPorts.append(port2add)
			 
		files = document.find('Files')
		for file in files.findall('File'):
			fileItem = Item(file.attrib['name'], file.attrib['type'], file.attrib['location'])
			self.files.append(fileItem)
	
    def saveModelDescriptionToXML(self, xmldir):
		modelDescription = Element('modelDescription')
		modelItem = SubElement(modelDescription, 'Model', name=str(self.model.name), type=str(self.model.type), description=str(self.model.description))
		
		### Inputs Ports
		inputs = SubElement(modelDescription, 'Inputs')
		for port in self.inputPorts: ### for each port in the inputs Port List
			inputport = SubElement(inputs, 'Port')  
			inputportname = SubElement(inputport, 'PortName')
			inputportname.text = str(port.name) ###add PortName value
			inputporttype = SubElement(inputport, 'Type')
			inputporttype.text = str(port.type) ###add Type value
			inputportdes = SubElement(inputport, 'Description')
			inputportdes.text = str(port.description) ###add des value
		
		### Outputs Ports
		outputs = SubElement(modelDescription, 'Outputs')
		for port in self.outputPorts: ### for each port in the inputs Port List
			outputport = SubElement(outputs, 'Port')  
			outputportname = SubElement(outputport, 'PortName')
			outputportname.text = str(port.name) ###add PortName value
			outputporttype = SubElement(outputport, 'Type')
			outputporttype.text = str(port.type) ###add Type value
			outputportdes = SubElement(outputport, 'Description')
			outputportdes.text = str(port.description) ###add des value
			
		### Outputs Ports		
		files = SubElement(modelDescription, 'Files')
		for fileItem in self.files: ### for each port in the inputs Port List
			file = SubElement(files, 'File', name=fileItem.name, type=fileItem.type, location=fileItem.description)
				
		###write into xml file
		output_file = open(xmldir, 'w')
		output_file.write('<?xml version = "1.0"?>')
		output_file.write(ElementTree.tostring(modelDescription))
		output_file.close()


print "-----------I am doing test class modelDescription----------------\n"

tagsi = ModelDescription()
tagsi.loadModelDescriptionFromXML('modelDescription.xml')
tagsi.saveModelDescriptionToXML('modelDescription-write.xml')

