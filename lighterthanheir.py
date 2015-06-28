from regulated_reader import RegulatedReader

class LighterThanHeir(RegulatedReader):
	def __init__(self):
		self.name  = 'lighterthanheir'
		self.title = "Lighter than Heir"
		self.link = "http://lighterthanheir.com/"
		self.description = "Lighter than Heir"
	
	def getnext(self, soup):
		return 'http://lighterthanheir.com'+soup.find('a', class_="next", rel="next").get('href')

	def getinfo(self, soup):
		return {
			'title': soup.find(id='newsheader').text,
			'description': str(soup.find(id='comicbody'))+str(soup.find(id='newsarea'))
		}

LighterThanHeir().build()
