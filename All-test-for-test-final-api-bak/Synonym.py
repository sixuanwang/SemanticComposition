import sys
import urllib2
import HTMLParser



from HTMLParser import HTMLParser
# create a subclass and override the handler methods
class LinksParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  def handle_starttag(self, tag, attributes):
    if tag != 'a':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class' and value == 'common-word':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'a' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)

# instantiate the parser and fed it some HTML, return a list
def synonyms(word):	
	if (word.isupper):
		response = urllib2.urlopen('http://thesaurus.com/browse/' + word)
		html = response.read()
		parser = LinksParser()
		parser.feed(html)
		response.close()  # best practice to close the file
		
		exceptList = ('','\r\n','star')
		
		wordList = []
		if (parser.data): 
			for v in parser.data:
				v = v.strip()
				if (v not in exceptList):
					wordList.append(v)			
		return wordList
	else:
		wordElseList = []
		return wordElseList
		
def check_synonym(word, word2):
	"""checks to see if word and word2 are synonyms"""
	try:
		synsets = synonyms(word) #check the first word's synonyms
		if word2 in synsets:
			return 1		
		synsets2 = synonyms(word2) #check the second word's synonyms
		if word in synsets2:
			return 1		
		return 0
	except: 
		return 0

'''
print check_synonym('number','service')
print check_synonym('good','nice')
print check_synonym('numbers','number')
print check_synonym('tag','tree')
print check_synonym('tree','trember')
print check_synonym('window','door')
print check_synonym('pair','two')
print check_synonym('two','twins')
print check_synonym('couple','mates')
print check_synonym('twins','combine')
print check_synonym('team','pair')
#print abbreviation('slogan')
'''

