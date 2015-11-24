from regulated_reader import RegulatedReader

class WapsiSquare(RegulatedReader):
	def __init__(self):
		self.name  = 'wapsisquare'
		self.title = "Wapsi Square"
		self.link = "http://wapsisquare.com/"
		self.description = "Slice of supernatural life YA comic PG-13 to R"
	
	def getnext(self, soup):
		return soup.find(id="sidebar-over-comic").find('a',class_="comic-nav-next").get('href')

	def getinfo(self, soup):
		return {
			'title': soup.find('h2',class_="post-title").text,
			'description': str(soup.find(id='comic'))+str(soup.find(id='content'))
		}

WapsiSquare().build()
