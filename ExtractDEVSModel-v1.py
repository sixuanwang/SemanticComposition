#2014-7-7: read DEVS models to a file
#input: a directory that contains model folders, each folder has many MA models.  
#output: a file contains the following information
#ModelPackageName |	ModelName (ma)	| Component | Output | Inport

from __future__ import print_function
import os 
import sys

modelDir = 'W:\[DEVSModel]\MA-DEVS'
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
		print('#################ModelProject ', modelCount, ' #########################', file=outputTestResults) # for readability
		lastMAfilePath = currentMAfilePath
	
	print(MAfilePathSplit[-2] + ' | ' + MAfilePathSplit[-1].split('.')[0] + ' | ', file=outputTestResults)

	#get content of each MA file from "MAfile"
	#each "[]"
	#each "components"
	#each "in"
	#each "out"	
	with open(MAfile) as f:
		for line in f:
			if line.startswith('[') or line.startswith('components') or line.startswith('in') or line.startswith('out'):
				print(line, end="", file=outputTestResults)
	
	print('', file=outputTestResults)
	
outputTestResults.close()
print ("DONE!")

'''
#read API, now the API is a single line, only read I and O parameters, each parameter can have more than one tag
ApiList = {}
ApiCount = 1
def read_APIs(line):  
	global ApiCount
	lineList = line.split('|')
	if (len(lineList)!=5 ):
		return
	else:
		ApiRead  = {}
		ApiRead['I']=[]
		ApiRead['O']=[]
		#add child note	  ApiRead['I'] ApiRead['O']	

		readParameterList_I =lineList[2].strip().split('&')
		
		for readParameter in readParameterList_I:
			readParameter = readParameter.strip()
			tagsInParameter_I = readParameter.split(' ')
			for elementInTags in tagsInParameter_I:
				if elementInTags.strip() == '':
					del elementInTags			
			ApiRead['I'].append(tagsInParameter_I)
		
		readParameterList_O = lineList[3].strip().split('&')
		
		for readParameter in readParameterList_O:
			tagsInParameter_O = readParameter.strip().split(' ')
			for elementInTags in tagsInParameter_O:
				if elementInTags.strip() == '':
					del elementInTags
			ApiRead['O'].append(tagsInParameter_O)
		
		ApiList[ApiCount] = ApiRead
		ApiCount += 1

with open(inputApis) as f:
	for line in f:
		read_APIs(line) #parse the line through various functions
'''


	
			
			
	
			
			










