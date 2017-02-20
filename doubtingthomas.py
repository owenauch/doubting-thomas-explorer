# Doubting Thomas Explorer:
# A python script to explore the bible by scraping cross references
#
# Matthew 28:17 -- "When they saw him, they worshiped him; but some doubted."

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import ssl
from sys import version_info

#base url
base = "https://www.biblegateway.com/passage/"

#verse to start our journey with
start_verse = "John 10:10"

# list of all verse found so far
verse_list = []

# A verse object, with info on the verse, as well as what it's linked to
class Verse:
	#constructor:
	# each verse has a book, chapter, verse, as well as an array of reference pointing in and out
	def __init__(self, url):
		self.book = self.get_book()
		self.chapter = self.get_chapter()
		self.verse = self.get_verse()
		self.refsIn = []
		self.refsOut = []
		self.url = url
		self.baseurl = "https://www.biblegateway.com/passage/?search="

	# get book name from url query string
	def get_book(self):
		book = self.url.split("+", 1)[0]
		return book

	# get chapter name from url query string
	def get_chapter(self):
		chapter = self.url.split("+", 1)[1].split("%", 1)[0]
		return chapter

	# gets verse from the url query string
	def get_verse(self):
		verse = self.url.split("%3A", 1)[1]
		return verse

	# adds a reference in to refsIn array
	# need to pass in a Verse object
	def add_ref_in(self, refIn):
		self.refsIn.append(refIn)

	# adds several references out to refsOut array
	# need to pass in an array of Verse objects
	def add_ref_out(self, refsOut):
		for verse in refsOut:
			self.refsOut.append(verse)

	#get full url for searching
	def get_full_url(self):
		return self.baseurl + self.url



#verify set to false for scrape
def verify_false():
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	return ctx

# create verse object for first verse and place in verse_list
def make_first_verse(verse):
    url = verse.replace(" ", "+")
    url = verse.replace(":", "%3A")
	start_verse = Verse(url)
	verse_list.append(start_verse)
	return start_verse

#open and soupify
def soupify(url):
    ctx = verify_false()
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

#get link for first cross-referenced verse
def get_next_url(soup):
    crossref_div = soup.find('div', class_='crossrefs')
    return crossref_div
