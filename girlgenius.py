from regulated_reader import RegulatedReader

class GirlGenius(RegulatedReader):
	def __init__(self):
		self.name  = 'girlgenius'
		self.title = "Girl Genius"
		self.link = "http://www.girlgeniusonline.com/comic.php"
		self.description = "Girl Genius Online Comic"
	
	def getnext(self, soup):
		return soup.find(id='topnext').get('href')

	def getinfo(self, soup):
		return {
			'title': 'Girl Genius for '+soup.find(id='datestring').text,
			'description': str(soup.find(id='comicbody'))
		}

GirlGenius().build()
