import feedparser
import urllib
import os
from bs4 import BeautifulSoup
import datetime

feed_dir = "./feeds/"
text_dir = "./feeds_text/"

#read list of feeds
def read_feeds(filename):
	feeds = open(filename, 'r')
	feeds = feeds.read().split('\n')
	return feeds


#get all feeds given feed filename
def write_feeds(filename):
	feeds = read_feeds(filename)
	count = 0
	
	date_path = make_date_dir(feed_dir)

	for feed in feeds:
		feed = feed.split('|')
		print feed
		url = feed[1]
		name = feed[0]
		parsed = feedparser.parse(url)
		entries = parsed.entries
		print '## ' + name + ' ##'
		for entry in entries:
			feed_write = open(date_path+name+'_'+str(datetime.datetime.now())+'_'+str(count)+'.html', 'w')
			content = urllib.urlopen(entry['link']).read()
			feed_write.write(content)
			count += 1

#translate the feeds into just the news stories
def translate_html():
	date_text_path = make_date_dir(text_dir)
	date_feed_dir = make_date_dir(feed_dir)

	to_remove = []
	for f in os.listdir(date_feed_dir):
		d_html = open(date_feed_dir+f, 'r')
		doc_html = d_html.read()
		write_doc = open(date_text_path+f+'.txt', 'w')
		soup = BeautifulSoup(doc_html)
		article_text = get_text(soup, f)
		write_doc.write(article_text)
		write_doc.close()
		d_html.close()
		to_remove.append(date_feed_dir+f)

	#remove all files
	for path in to_remove:
		os.remove(path)

def make_date_dir(base_dir):
	#get date for file name
	dt = datetime.datetime.now()
	month = dt.month
	if month < 10:
		month = "0" + str(month)

	day = dt.day
	if day < 10:
		day = "0" + str(day)

	dt = str(dt.year) + "-" + str(month) + "-" + str(day)
	date_path = base_dir+"/"+dt+"/"

	if not os.path.exists(date_path):
		os.makedirs(date_path)

	return date_path

def get_text(soup, file_name):
	name = file_name.split('_')[0]
	if name == "nasdaq":
		article_text = soup.find("div", id="articleText")
		return article_text.get_text().encode('utf-8')
	elif 'cnn' in name or 'marketwatch' in name:
		ps = soup.find_all("p")
		text = ""
		for p in ps:
			text += p.get_text().encode('utf-8') + " "

		return text
	elif 'reuters' in name:
		article_text = soup.find("span", id="articleText")
		return article_text.get_text().encode('utf-8')

	return 'NO NAME FOUND'