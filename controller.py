import rss_news as RSS
import stock_list as STOCKS
import file_sentiment as SENT
import hist_data as HIST
import cPickle as pickle
import time

from Tkinter import *
import operator

pickle_file = "./pickles/single_word_dict.p"
feed_loc = "./setup/rss_feeds.txt"

def download_rss():
	RSS.write_feeds(feed_loc)
	RSS.translate_html()

def add_to_dictionary():
	word_dict = pickle.load(open(pickle_file, 'rb'))
	word_dict = SENT.value_words(word_dict)
	pickle.dump(word_dict, open(pickle_file, 'wb'))
	print "sorting..."
	sorted_words = sorted(word_dict.iteritems(), key=lambda data: data[1][0])
	for word in sorted_words:
		print word

def add_to_bigram_dictionary():
	word_dict = {}
	word_dict = SENT.value_words_bigram(word_dict)
	sorted_words = sorted(word_dict.iteritems(), key=lambda data: data[1][0])
	for word in sorted_words:
		print word

if __name__ == '__main__':
	print "Downloading RSS..."
	download_rss()
	print "Done with downloading/turning into text"
	#time.sleep(.5)
	print "Doing BIGRAM sentiment analysis...."
	#add_to_bigram_dictionary()
	print "Finished adding new words to dict"


#Draw Clusters
'''
master = Tk()

w = Canvas(master, width=400, height=400)
w.pack()

w.create_line(0, 0, 200, 100)

mainloop()'''
