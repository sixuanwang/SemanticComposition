import sys

outputf = open('taginfo_parsed.txt', 'w') 

toprint = ""
isDocument = 0;


with open('taginfo - Copy.xml') as f:
	for line in f:
		if(line.find('<document>')!=-1):  #<document>
			isDocument = 1;
			
		if(line.find('<name>')!=-1):    #<name>
			line = line.strip()
			line = line.replace('<name>','')
			line = line.replace('</name>','')		
			toprint = toprint + line + ": "
			
		if(line.find('<weight>')!=-1):    #<weight>
			line = line.strip()
			line = line.replace('<weight>','')
			line = line.replace('</weight>','')		
			toprint = toprint + line + " | "
			
		if(line.find('</document>')!=-1):  #output
			outputf.write(toprint+"\n")
			toprint = ""
			
outputf.close()