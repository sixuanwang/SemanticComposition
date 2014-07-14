import sys
import urllib2
import HTMLParser



from HTMLParser import HTMLParser
# create a subclass and override the handler methods
class LinksParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = ''

  def handle_starttag(self, tag, attributes):
    if tag == 'h1':
      self.recording = 1
  
  def handle_endtag(self, tag):
    if tag == 'h1':
		self.recording = 0

  def handle_data(self, data):
    self.data = data

# instantiate the parser and fed it some HTML, return a word
def plural(word):	
	try: 
		response = urllib2.urlopen('http://www.merriam-webster.com/dictionary/'+word)
		html = response.read()
		parser = LinksParser()
		parser.feed(html)
		response.close()  # best practice to close the file
		if (parser.data): 
			return parser.data.strip()
		else: 
			return 'NotFound'
	except Exception:
		return 'NotFound'

	