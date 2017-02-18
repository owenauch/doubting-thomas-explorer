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

#bible version
version = "NIV"

#verify set to false for scrape
def verify_false():
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	return ctx

#make verse string usable as a url query parameter
def urlify_verse(verse):
    verse = verse.replace(" ", "+")
    verse = verse.replace(":", "%3A")
    return verse

#for putting it back at the end
def versify_url(url):
    verse = url.replace(" ")

#get verse query string
def get_start_url(verse):
    url_verse = urlify_verse(verse)
    verse_query = "?search=" + url_verse + "&version=" + version
    start_url = base + verse_query
    return start_url

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

#test as we go
url = get_start_url(start_verse)
soup = soupify(url)
print(get_next_url(soup))
