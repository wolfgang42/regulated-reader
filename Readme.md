# About
Regulated Reader is a program I wrote in an attempt to cut down on the amount of binge-reading of webcomics I was doing.
It goes through the archives of a site and generates an RSS feed that you can add to your RSS reader.

# Usage
## Getting started
To install dependencies:
```bash
virtualenv venv2
source venv2/bin/activate
pip install -r requirements.txt
```

## Using a script
Pick a series you want to follow. For this example, we'll use Girl Genius, the script for which is `girlgenius.py`.
You'll also need a URL you want to start with; here we'll use the first one, but you can pick any URL (in case you want to start in the middle of the series, for example if you've read the first half already.)
```bash
python girlgenius.py init http://girlgeniusonline.com/comic.php?date=20021104
```
This will create `girlgenius.json` and `girlgenius.rss`, with one entry: the URL you initialized it with.
Now run
```bash
python girlgenius.py
```
This will add the next comic in the series to the RSS feed. Every time the script is run, another comic is added.

You'll probably want to set up a cron job to add to the feed on your desired schedule; for example, here's my crontab entry for xkcd, to fill in between the Monday, Wednesday, and Friday updates:
```cron
37 2 * * tue,thu,sat cd /var/www/static/regulated-reader; venv2/bin/python xkcd.py
```
I have this set up to run on my webserver, so I point my RSS reader to http://static.linestarve.com/regulated-reader/xkcd.rss

Please be considerate: pick a random number for the minute so the website isn't hammered by everyone's cronjobs fetching content at the top of the hour.

## Writing a new script
Writing a new script is very easy. Here's the full script of `girlgenius.py`:
```python
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
```

This breaks down into three functions:
* `__init__()` should set up information about the feed. This is self-explanatory.
* `getnext()` is passed a BeautifulSoup object, and should return the full URL to the next entry in the series. This should be simply a matter of finding the right selector and getting its `href`.
* `getinfo()` is passed a BeautifulSoup object, and should return a dictionary of `title` and `description`.
	`description` can contain HTML; you will probably just find a selector in the document that contains the content you want.
	**Important:** `description` *must* be a string: if you return a BeautifulSoup object your script will crash with `TypeError: 'NoneType' object is not callable` when it tries to generate the RSS file.

Don't forget the `ClassName().build()` at the end of the script: if it's missing nothing will happen.

If you write a useful script, send a pull request!

# Bugs
* Scripts are scattered around in this directory. I'd like to put them in a subdirectory, but I keep running into issues with Python library paths and the like.
