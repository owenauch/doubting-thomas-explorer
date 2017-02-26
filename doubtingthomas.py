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
start_verse_name = "1 John 3:16"

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
        book = self.url.rpartition("+")[0]
        book = book.replace("+", " ")
        return book

    # get chapter name from url query string
    def get_chapter(self):
        chapter = self.url.split("+")[-1].split("%", 1)[0]
        return chapter

    # gets verse from the url query string
    def get_verse(self):
        verse = self.url.split("%3A", 1)[1]
        return verse

    # adds a reference in to refsIn array
    # need to pass in a Verse object
    def add_ref_in(self, refIn):
        self.refsIn.append(refIn)
        return self

    # adds several references out to refsOut array
    # need to pass in an array of Verse objects
    def add_ref_out(self, refOut):
        self.refsOut.append(refOut)
        return self

    #get full url for searching
    def get_full_url(self):
        return self.baseurl + self.url

    #allows == to work
    def __eq__(self, other):
        if (self.get_book() != other.get_book()):
            return False
        if (self.get_chapter() != other.get_chapter()):
            return False
        if (self.get_verse() != other.get_verse()):
            return False
        return True

    #__str__ isn't feeling it so I'm doing this I guess
    def get_name(self):
        return (self.book + " " + self.chapter + ":" + self.verse)



#verify set to false for scrape
def verify_false():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# create verse object for first verse and place in verse_list
def make_first_verse(verse):
    #books with space make this harder -- ex. 1 John
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
def get_next_verses(verse, num):
    soup = soupify(verse)
    crossref_div = soup.find("div", class_="crossrefs")

    #gets all list elements in crossref_div
    #make sure it has cross-references
    if (crossref_div):
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

                # filter refsOut for duplicates
                if (new_verse not in verse.refsOut):
                    verse.refsOut.append(new_verse)

                #checks if verse already exists in verse_list
                #if it is, adds the new in reference as long as it won't be duplicating a refIn
                # if it's already in the list, return
                if (new_verse in verse_list):
                    index = verse_list.index(new_verse)
                    if (verse not in verse_list[index].refsIn):
                        new_verse = verse_list[index].add_ref_in(verse)
                        verse_list[index] = new_verse
                    return;
                #otherwise, adds it to the list
                else:
                    verse_list.append(new_verse)
                if (new_verse in verse.refsIn):
                    return
                if (num < 25):
                    print ("Verse: " + new_verse.get_name())
                    print "Crossrefs:"
                    for r in new_verse.refsOut:
                        print "    " + r.get_name()
                    num = num + 1
                    get_next_verses(new_verse, num)


#first step
start_verse = make_first_verse(start_verse_name)
get_next_verses(start_verse, 1)
print "+++++++++++++++++++++++++"
for v in verse_list:
    print "Verse: " + v.get_name()
    print "Refs In:"
    for refIn in v.refsIn:
        print "    " + refIn.get_name()
    print "Refs Out:"
    for refOut in v.refsOut:
        print "    " + refOut.get_name()
