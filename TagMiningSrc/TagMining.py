
#July 10, 2014: 

#July 9, 2014: tag mining 
#example: DEVS models 
#change the online source to the python build-in functions

# get the service signature 
# should be <title, type, endpoint(URI), method/(relative URI), input, output, description>
# here initial work done: <input, output, description>
 
from __future__ import print_function
import sys
import re
import Abbreviation
import POS
import Plural

inputFile = 'ExtractDEVSModel-beforeTagMining.txt'
outputFile = file('ExtractDEVSModel-afterTagMining.txt', 'w')

#for D: description, separate by everything
def tagMiningFunctions(line):
	returnlist = []
	
	#if starts with sth (e.g. like ###), then not mine, just return the original line
	if line.startswith('###'):
		returnlist.append(line)
		return returnlist
	
	#1.tokenize the line using delimiters
	elif line  in abbreviationFilterList:  #single word
		if (line):
			returnlist.append(line.lower())
	else:
		words_in_line = tokenize_delimiters(line)		
			
		for word_in_line in words_in_line:  
			if ('|' in word_in_line):
				returnlist.append('|')
			elif len(word_in_line) > 1: #added Dec 05
				#5. abbreviation
				if word_in_line in abbreviationFilterList:
					if (word_in_line):
						returnlist.append(word_in_line.lower())
				else:
					if(word_in_line.isupper() and word_in_line not in abbreviationFilterList):
						words_after_abbre = Abbreviation.abbreviation(word_in_line)
					else:
						words_after_abbre = [word_in_line,]
							
					for word_after_abbre in words_after_abbre:
						#2. estone_split 
						word_after_estone = estone_splitword(word_after_abbre)
						
						for each_word in word_after_estone:							
							#3. remove digital
							if not each_word.isdigit():
								###SIXUAN: USE THE PYTHON GIT TO REALISE THESE FUNCTION
								###uncomment if want to check plural and POS, note that if do so, it will use web site calls, take much time, 
								### this can be improved via python build in function
								###4. plural -> single, verb conjugation:  www.merriam-webster.com									
								###6. POS www.merriam-webster.com, after this website, the plural is already single, same as verb								
								#wordAfterPOS = POS.POSwithCheckList(each_word, POSCheckList) #Changed Dec 05, if a word has multi POS, as long as it can be noun, fine, we take it
								#if (wordAfterPOS not in stopWordsFilterList):
								#	if (wordAfterPOS):
								#		returnlist.append(wordAfterPOS)
								
								###comment is if want plural and POS above
								if (each_word not in stopWordsFilterList):
									if (each_word):
										returnlist.append(each_word)
	#sorted(set(returnlist),key=returnlist.index) #7. remove duplicated words
	return returnlist 

#filter of abbreviation
abbreviationFilterList = set(['GET','PUT','DELETE','POST','OPTION','DEVS','Cell-DEVS', 'Cell-DEVS', 'CD++', 'PCD++', '3D', '2D', 'query', 'zip', 'ip' 'id'])

#checklist of POS 'verb','adjective'
POSCheckList = set(['noun', 'verb'])

#stop words, not used yet
stopWordsFilterList = set(['a','its','', 'get','post','put','delete', 'option','None', 'NotFound'])
	
delimiters = (' ', '/', '"', '#', '\\', '$', '?', '*', '+', '-' , '.',
	          '(', ')', '[', ']', '{', '}', '@',
               ',', ':', '`', '=', ';', '+=',  '-=',
               '*=', '/=', '//=', '%=', '&=', '|=', '^=', '>>=', '<<=', '**=')

"""split the line using all delimiters"""
def tokenize_delimiters(line):
	stack = [line,]

	for delimiter in delimiters:
		for i, substring in enumerate(stack):
			substack = substring.split(delimiter)
			stack.pop(i)
			for j, _substring in enumerate(substack):
				stack.insert(i+j, _substring.strip())
	
	while '' in stack:
		stack.remove('')

	return stack

    
def estone_splitword(word):
    #word is input
	word = word[0:1].upper() + word[1:]
	wordfind = re.findall('[A-Z][^A-Z]+', word)
	
	if wordfind:
		for i, subword in enumerate(wordfind):
			wordfind[i] = wordfind[i].lower()
		return wordfind
	else:
		wordElseList = []
		wordElseList.append(word.lower())
		return wordElseList
	
	
'''main function'''

#tagMiningList = []
#tagMiningList = parse_line_D()
#print tagMiningList   

with open(inputFile) as f:
	for line in f:
		tagMiningList = []
		tagMiningList = tagMiningFunctions(line) #parse the line through various functions
		print (' '.join(tagMiningList), file=outputFile)