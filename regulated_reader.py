from bs4 import BeautifulSoup
import requests, PyRSS2Gen
import json, time, datetime, sys, os

def _print_usage():
	sys.stderr.write('Usage: \n')
	sys.stderr.write(sys.argv[0]+" init [URL] - set up the RSS feed\n")
	sys.stderr.write(sys.argv[0]+" - Generate an RSS feed with the next item\n")
	sys.exit(1)

class RegulatedReader():
	def add_item(self, feed, next_url):
		feed_item = self.getinfo(_get_soup(next_url))
		feed_item['link'] = next_url
		feed_item['pubDate'] = time.time()
		
		feed.append(feed_item)
		
		with open(self.name+'.rss', 'w') as f:
			_compose_pyrss2_tree(feed, self.title, self.link, self.description).write_xml(f)
		
		with open(self.name+'.json', 'w') as f:
			json.dump(feed, f)
		
	def build(self):
		if len(sys.argv) == 1: # Build the RSS feed
			with open(self.name+'.json') as f:
				feed=json.load(f)
			next_url = self.getnext(_get_soup(feed[-1]['link']))
		elif len(sys.argv) == 3 and sys.argv[1] == 'init':
			if os.path.exists(self.name+'.json'):
				sys.stderr.write('That feed has already been initialized. Please delete '+self.name+'.json if you wish to start over.\n')
				sys.exit(2)
			feed = []
			next_url = sys.argv[2]
		else:
			_print_usage()
		
		self.add_item(feed, next_url)

def _get_soup(url):
	r = requests.get(url)
	r.raise_for_status()
	return BeautifulSoup(r.text)

def _compose_pyrss2_tree(feed, title, link, description):
	items = []
	for item in feed:
		items.append(PyRSS2Gen.RSSItem(
			title = item['title'],
			link  = item['link'],
			description = item['description'],
			guid = PyRSS2Gen.Guid(item['link']),
			pubDate = datetime.datetime.fromtimestamp(item['pubDate']),
		))
	
	return PyRSS2Gen.RSS2(
		title = title,
		link = link,
		description = description,
		lastBuildDate = datetime.datetime.now(),
		items = items,
	)
