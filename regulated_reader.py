from bs4 import BeautifulSoup
import requests, PyRSS2Gen
import json, time, datetime, sys, os

def _get_soup(url):
	r = requests.get(url)
	r.raise_for_status()
	return BeautifulSoup(r.text)

def _print_usage():
	sys.stderr.write('Usage: \n')
	sys.stderr.write(sys.argv[0]+" init [URL] - set up the RSS feed\n")
	sys.stderr.write(sys.argv[0]+" - Generate an RSS feed with the next item\n")
	sys.exit(1)

def build_rss(comicname, title, link, description, fn_getnext, fn_getinfo):
	if len(sys.argv) == 1: # Build the RSS feed
		with open(comicname+'.json') as f:
			feed=json.load(f)
		next_url = fn_getnext(_get_soup(feed[-1]['link']))
	elif len(sys.argv) == 3:
		if sys.argv[1] == 'init':
			if os.path.exists(comicname+'.json'):
				sys.stderr.write('That feed has already been initialized. Please delete '+comicname+'.json if you wish to start over.\n')
				sys.exit(2)
			feed = []
			next_url = sys.argv[2]
		else:
			_print_usage()
	else:
		_print_usage()
	
	feed_item = fn_getinfo(_get_soup(next_url))
	feed_item['link'] = next_url
	feed_item['pubDate'] = time.time()
	
	feed.append(feed_item)
	
	with open(comicname+'.rss', 'w') as f:
		_compose_pyrss2_tree(feed, title, link, description).write_xml(f)
	
	with open(comicname+'.json', 'w') as f:
		json.dump(feed, f)

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
