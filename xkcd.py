from regulated_reader import RegulatedReader

class Xkcd(RegulatedReader):
	def __init__(self):
		self.name  = 'xkcd'
		self.title = "xkcd"
		self.link = "http://xkcd.com"
		self.description = "A webcomic of romance and math humor."
	
	def getnext(self, soup):
		return 'http://xkcd.com'+soup.find("a", rel="next").get('href')

	def getinfo(self, soup):
		return {
			'title': soup.find(id='ctitle').text,
			'description': str(soup.find(id='comic'))
		}

Xkcd().build()
