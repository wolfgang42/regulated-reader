from regulated_reader import RegulatedReader

class Zap(RegulatedReader):
	def __init__(self):
		self.name  = 'zap'
		self.title = "Zap!"
		self.link = "http://www.zapcomic.com/"
		self.description = "Zap!"
	
	def getnext(self, soup):
		return soup.find(class_="comicnav_top").find('a',class_="next-comic-link").get('href')

	def getinfo(self, soup):
		return {
			'title': soup.find('h1').text,
			'description': str(soup.find(id='comic2'))
		}

Zap().build()
