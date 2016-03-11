from regulated_reader import RegulatedReader
from urlparse import urljoin

class FlakyPastry(RegulatedReader):
	def __init__(self):
		self.name  = 'flakypastry'
		self.title = "Flaky Pastry"
		self.link = "http://http://flakypastry.runningwithpencils.com/"
		self.description = "A webcomic about nothing in particular"
	
	def getnext(self, soup):
		return 'http://flakypastry.runningwithpencils.com/comic.php'+soup.find('img', src="gfx/btn_next.jpg").parent.get('href')

	def getinfo(self, soup):
		# Turn relative image URL into absolute
		image = soup.find('img',usemap='#ImageMap')
		image['src'] = 'http://flakypastry.runningwithpencils.com/'+image['src']
		# Turn relative URLs in description into absolute links
		desc = soup.find(class_='rss-content')
		for link in desc.find_all('a'):
			link['href'] = urljoin('http://flakypastry.runningwithpencils.com/comic.php', link['href'])
		
		return {
			'title': soup.find(class_='rss-title').text,
			'description': str(image)+'<div>'+str(desc)+'</div>'
		}

FlakyPastry().build()
