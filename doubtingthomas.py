# Doubting Thomas Explorer:
# A python script to explore the bible by scraping cross references
#
# Matthew 28:17 -- "When they saw him, they worshiped him; but some doubted."

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import ssl
from sys import version_info
import re

#base url
base = "https://www.biblegateway.com/passage/"

#verse to start our journey with
start_verse_name = "John 10:10"

# list of all verse found so far
verse_list = []

# A verse object, with info on the verse, as well as what it's linked to
class Verse:
	#constructor:
	# each verse has a book, chapter, verse, as well as an array of reference pointing in and out
	def __init__(self, url):
		self.url = url
		self.baseurl = "https://www.biblegateway.com/passage/?search="
		self.book = self.get_book()
		self.chapter = self.get_chapter()
		self.verse = self.get_verse()
		self.refsIn = []
		self.refsOut = []

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
	def add_ref_out(self, refOut):
		self.refsOut.append(refOut)

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
	url = url.replace(":", "%3A")
	start_verse = Verse(url)
	verse_list.append(start_verse)
	return start_verse

#open and soupify verse
def soupify(verse):
    ctx = verify_false()
    url = verse.get_full_url()
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

#parses a long url of multiple verses into seperate verse urls
def parse_crossref_url(href):
    urls = href.split('search=', 1)[1].split('%2C')
    urls[-1] = urls[-1].split('&version', 1)[0]
    return urls

#the biggie
#gets all the verses crossreferenced by the input verse,
#saves then to verse_list, then calls get_next_verses on all of them
def get_next_verses(verse):
    soup = soupify(verse)
    crossref_div = soup.find("div", class_="crossrefs")

    #gets all list elements in crossref_div
    crossref_li = crossref_div.find_all("li")

    #gets href for each a element to a cross-referenced verse
    #puts in list hrefs_list
    #each href is in the form /passage/?search=<verse1url>%2C<verse2url>&version=NIV
    hrefs_list = []
    for li in crossref_li:
        full_link = li.find("a", class_="crossref-link")['href']
        hrefs_list.append(full_link)

    #get all the reference urls, make them into verses
    #save properties of them, save them to verse list, and call on them
    for ref in hrefs_list:
        refs_list = parse_crossref_url(ref)
        for ref in refs_list:
            new_verse = Verse(ref)
            new_verse.add_ref_in(verse)
            verse.add_ref_out(new_verse)
            print new_verse.get_book() + new_verse.get_chapter() + new_verse.get_verse()
            get_next_verses(new_verse)


#first step
start_verse = make_first_verse(start_verse_name)
get_next_verses(start_verse)
