from regulated_reader import RegulatedReader
import requests
from bs4 import BeautifulSoup

class Gaia(RegulatedReader):
	def __init__(self):
		self.name  = 'gaia'
		self.title = "Gaia"
		self.link = "http://www.sandraandwoo.com/gaia"
		self.description = "Gaia: Will you come along?"
	
	def get_soup(self, url):
		# HACK I have no idea why this is necessary
		r = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36'})
		r.raise_for_status()
		return BeautifulSoup(r.text)
	
	def getnext(self, soup):
		return soup.select('.post-comic .nav-next a')[0].get('href')

	def getinfo(self, soup):
		return {
			'title': soup.select('.post-comic h2')[0].text,
			'description': str(soup.find(id='column'))
		}

Gaia().build()
