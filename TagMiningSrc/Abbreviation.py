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
    if tag != 'p':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class' and value == 'desc':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'p' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      self.data.append(data)

# instantiate the parser and fed it some HTML, return a list
def abbreviation(word):	
	if (word.isupper):
		response = urllib2.urlopen('http://www.abbreviations.com/' + word)
		html = response.read()
		parser = LinksParser()
		parser.feed(html)
		response.close()  # best practice to close the file
		if (parser.data): 
			return parser.data[0].split(' ')
		else: 
			wordElseList = []
			wordElseList.append(word)
			return wordElseList
	else:
		wordElseList = []
		wordElseList.append(word)
		return wordElseList
	

