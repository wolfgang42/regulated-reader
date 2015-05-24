import regulated_reader

def getnext(soup):
	return soup.find(id='topnext').get('href')

def getinfo(soup):
	return {
		'title': 'Girl Genius for '+soup.find(id='datestring').text,
		'description': str(soup.find(id='comicbody'))
	}

regulated_reader.build_rss('girlgenius',
		"Girl Genius",
		"http://www.girlgeniusonline.com/comic.php",
		"Girl Genius Online Comic",
		getnext, getinfo)
