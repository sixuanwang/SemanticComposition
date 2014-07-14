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
    if tag != 'span':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class' and value == 'main-fl':
        break
    else:
      return
    self.recording = 1
  
  def handle_endtag(self, tag):
    if tag == 'span' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)

from sgmllib import SGMLParser
# create a subclass and override the handler methods - plural
class LinksParserPlural(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_h1 = ""
		self.recording = 0
		self.data = []

	def start_h1(self, attrs):
		self.is_h1 = 1
	def end_h1(self):
		self.is_h1 = ""
	def handle_data(self, text):
		if self.is_h1 == 1:
			self.data.append(text)
	  
# instantiate the parser and fed it some HTML, return a word
def POS(word):	
	try: 
		response = urllib2.urlopen('http://www.merriam-webster.com/dictionary/'+word)
		html = response.read()
		
		parser = LinksParser()
		parser.feed(html)
		
		pluralParser = LinksParserPlural()
		pluralParser.feed(html)
		
		response.close()  # best practice to close the file
		if (parser.data and pluralParser.data): 
			return parser.data[0].strip() + "_" + pluralParser.data[0].strip()
		else: 
			return 'NotFound'
	except Exception:
		return 'NotFound'

#Dec05, 2013. see the POS of word, whether it is in POSCheckList, if so, than return the single form . 
def POSwithCheckList(word, POSCheckList):	
	try: 
		response = urllib2.urlopen('http://www.merriam-webster.com/dictionary/'+word)
		html = response.read()
		
		parser = LinksParser()
		parser.feed(html)
		
		pluralParser = LinksParserPlural()
		pluralParser.feed(html)
		
		response.close()  # best practice to close the file
		if (parser.data and pluralParser.data and  pluralParser.data[0]): 
			for pos in parser.data: 
				if pos in POSCheckList:
					return pluralParser.data[0].strip()
		else: 
			return 'NotFound'
	except Exception:
		return 'NotFound'
	
#print POS('heat', ['noun'])