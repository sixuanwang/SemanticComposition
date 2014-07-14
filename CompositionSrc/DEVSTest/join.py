from __future__ import print_function
inputfile1 = 'ExtractDEVSModelResults-NamePorts-selected-supposed-generated-v2 - manual tag.txt'
inputfile2 = 'ExtractDEVSModelResults-containLinks.txt'
outputfile = file('ExtractDEVSModelResults-containLinks&manualtag.txt', 'w')

'''
fileList1 = []
with open(inputfile1) as f:
	for line in f:
		fileList1.append(line)
		
fileList2 =[]
with open(inputfile2) as f:
	for line in f:
		fileList2.append(line)
		

for i,x in enumerate(fileList1):
	newLine = fileList1[i].strip('\n') + ' | '
	newLine = newLine.strip('\n')		
	newLine2 = newLine+ (fileList2[i].split('|'))[-1]	
	newLine2 = newLine2.strip('\n')
	print >> outputfile, newLine2
'''

for i in range (226):
	print(i, ':[], ', end="", file=outputfile)
outputfile.close()