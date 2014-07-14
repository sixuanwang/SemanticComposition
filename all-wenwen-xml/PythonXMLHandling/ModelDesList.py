
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
		modelDescription = Element('ModelDescription')
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

class ModelDescriptionList:
	"list of ModelDescription"
	def __init__(self, mdlist = {}):
		self.modelDescriptionList = mdlist ### dict: {'1': signature1, '2':signature2}
		self.totid = 0  

	#not test
	def saveModelDescription(self, modelDescription):
		self.totid = totid +1
		self.modelDescriptionList[totid] = modelDescription
		
	#not test
	def removeModelDescriptionByValue(self, modelDescription):
		if index == self.modelDescriptionList.index(modelDescription):
			del self.modelDescriptionList[index]
		
	#not test		
	def findModelDescriptionId(self, modelDescription):
		modelItem = modelDescription.model		
		for (k,v) in  self.modelDescriptionList.items(): 
			modelItem2 = v.model
			#only check the model item, not all, could be changed
			if(modelItem.name == modelItem2.name and modelItem.type == modelItem2.type and modelItem.description == modelItem2.description):
				return k
		return 0		
	
	#not test
	def removeModelDescriptionByID(self, id):
		if id in self.modelDescriptionList:
			del self.modelDescriptionList[id]
	
	def loadModelDescriptionListFromXML(self, xmldir):	
		document = ElementTree.parse(xmldir)
		
		for ts in document.findall('ModelDescription'):		
			modelTemp = ModelDescription()  ##to be saved
			
			model_name = ts.find('Model').attrib['name']
			model_type = ts.find('Model').attrib['type']
			model_description = ts.find('Model').attrib['description']
			modelItem = Item(model_name, model_type, model_description)	
			modelTemp.model = modelItem

			inlist = []
			##inputs = ts.find('Inputs')  
			for port in ts.findall('Inputs/Port'): 
				newport = Item(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
				inlist.append(newport)
				##modelTemp.inputPorts.append(newport)
			modelTemp.inputPorts = inlist
			
			##outputs = ts.find('Outputs')
			outlist = []
			for port in ts.findall('Outputs/Port'):
				port2add = Item(port.find('PortName').text, port.find('Type').text, port.find('Description').text)
				outlist.append(port2add)
				##modelTemp.outputPorts.append(port2add)
			modelTemp.outputPorts = outlist	 
			
			flist = []
			for file in ts.findall('Files/File'):				
				fileItem = Item(file.attrib['name'], file.attrib['type'], file.attrib['location'])
				flist.append(fileItem)
			modelTemp.files = flist
						
			self.modelDescriptionList[ts.attrib['id']] = modelTemp 
			print "inputports len ", len(modelTemp.inputPorts)
			modelTemp = None
		
	def printModelDescriptionList(self): 	
		for tid,ts in self.modelDescriptionList.items():  
			print('Model:', ts.model.name, ts.model.type, ts.model.description)
			for iport in ts.inputPorts:
				print('inputPort:', iport.name, iport.type, iport.description)
			for oport in ts.outputPorts:
				print('outputPorts:', oport.name, oport.type, oport.description)
			for file in ts.files:
				print('files:', file.name, file.type, file.description)
	
	def saveModelDescriptionListToXML(self, xmldir):	
		tslist = Element('ModelDescriptionList')
		for tid,ts in self.modelDescriptionList.items():  ### for all valus in dict 
			modelDescription = SubElement(tslist, 'ModelDescription', id=str(tid)) 
			#modelDescription = SubElement(tslist, 'ModelDescription') 
			### create a new ModelDescription Node
			modelItem = SubElement(modelDescription, 'Model', name=str(ts.model.name), type=str(ts.model.type), description=str(ts.model.description))
		
			print "AAA:", ts.model.name
		
			### Inputs Ports
			inputs = SubElement(modelDescription, 'Inputs')
			print "inputPortSize:", len(ts.inputPorts)
			for port in ts.inputPorts: ### for each port in the inputs Port List				
				inputport = SubElement(inputs, 'Port')  
				inputportname = SubElement(inputport, 'PortName')
				inputportname.text = str(port.name) ###add PortName value
				inputporttype = SubElement(inputport, 'Type')
				inputporttype.text = str(port.type) ###add Type value
				inputportdes = SubElement(inputport, 'Description')
				inputportdes.text = str(port.description) ###add des value
			
			### Outputs Ports
			outputs = SubElement(modelDescription, 'Outputs')
			for port in ts.outputPorts: ### for each port in the outputs Port List
				outputport = SubElement(outputs, 'Port')  
				outputportname = SubElement(outputport, 'PortName')
				outputportname.text = str(port.name) ###add PortName value
				outputporttype = SubElement(outputport, 'Type')
				outputporttype.text = str(port.type) ###add Type value
				outputportdes = SubElement(outputport, 'Description')
				outputportdes.text = str(port.description) ###add des value
				
			### Outputs Ports		
			files = SubElement(modelDescription, 'Files')
			print "fileAAA:", len(ts.files)
			for fileItem in ts.files: ### for each port in the inputs Port List
				file = SubElement(files, 'File', name=fileItem.name, type=fileItem.type, location=fileItem.description)
				
					
		###write into xml file
		output_file = open(xmldir, 'w')
		output_file.write('<?xml version = "1.0"?>')
		output_file.write(ElementTree.tostring(tslist))
		output_file.close()
		

print "-------------I am doing test class ModelDescriptionList! ---------\n"
tagsilist = ModelDescriptionList()
tagsilist.loadModelDescriptionListFromXML('modelDescriptionList.xml')

tagsilist.printModelDescriptionList()
	
tagsilist.saveModelDescriptionListToXML('modelDescriptionList-write.xml')
