#2014-7-8: read DEVS models to a file
#input: a directory that contains model folders, each folder has many MA models.  
#output: a file contains the following information
#ModelPackageName |	ModelName (ma)	| Output | Inport

from __future__ import print_function
import os 
import sys

modelDir = 'W:\[DEVSModel]\MA-DEVS-v2'
outputTestResults = file('ExtractDEVSModelResults.txt', 'w')

AllMAsList = []  #all the full filepath of MA files

#read all the MA files from folders
def readAllMAsUnderDir(_modelDir): 
    list_dirs = os.walk(_modelDir) 
    for root, dirs, files in list_dirs:      
        for f in files: 
			#only *.ma file
			fileName, fileExtention = os.path.splitext(f)
			if(fileExtention == '.ma'):
				AllMAsList.append(os.path.join(root, f))

readAllMAsUnderDir(modelDir)
			

lastMAfilePath = ''   #for the check of weather it is in a same ModelName, since each model name can have more than one MA files
currentMAfilePath = ''
modelCount = 0
			
for MAfile in AllMAsList:
	MAfilePathSplit = []
	MAfilePathSplit = MAfile.split('\\')
	#ModelName = MAfilePathSplit[-2]
	#Atomic/CoupledModel under the ModelName = MAfilePathSplit[-1]	
	
	currentMAfilePath = MAfilePathSplit[-2]
	if(currentMAfilePath != lastMAfilePath):
		modelCount =modelCount+1
		#print('\n#################ModelProject', modelCount, '-' , MAfilePathSplit[-2], ' #########################', file=outputTestResults) # for readability
		lastMAfilePath = currentMAfilePath
	
	MAfileName = MAfilePathSplit[-1].split('.')[0] #atomic or coupled name
	if(MAfileName.endswith('MA')):
		MAfileName = MAfileName[:-2]
	
	print(MAfilePathSplit[-2] + ' | ' + MAfileName + ' | ', end="", file=outputTestResults)

	#get content of each MA file from "MAfile"
	#each "[]"
	#each "components"
	#each "in"
	#each "out"	
	with open(MAfile) as f:
		inPortsLines = []
		outPortsLines = []
		linkLines = []
		
		for line in f:
		
			inportname=''
			outportname=''
			links=''
			
			#if line.startswith('[') or line.startswith('components') or line.startswith('in') or line.startswith('out'):
			if line.startswith('[') and not line.startswith('[top]'): #only the top parts
				break
						
			elif line.startswith('out'):   #for out, put together, get the second part split(':')[1], and remove '\n' [:-1]
				inportname = ((line.split(':')[1])[:-1]).strip()  
				if(inportname.lower() == 'out'): #make it more meaningful, if only OUT, add its modelname
					inportname = MAfileName
				outPortsLines.append(inportname)
			elif line.startswith('in'):  #for in, put together
				outportname = ((line.split(':')[1])[:-1]).strip()
				if(outportname.lower() == 'in'):
					outportname = MAfileName
				inPortsLines.append(outportname)
				
			elif line.startswith('Link'):  #for link, put together
				links = ((line.split(':')[1])[:-1]).strip()
				links = links +' , '
				if(links.lower() == 'link'):
					links = MAfileName
				linkLines.append(links)
		
														
		print(' '.join(outPortsLines), ' | ', end="", file=outputTestResults)
		print(' '.join(inPortsLines), ' | ', end="", file=outputTestResults)
		print(' '.join(linkLines), end="", file=outputTestResults)
	print('', file=outputTestResults)
	
outputTestResults.close()
print ("DONE!")



