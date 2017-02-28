import doubtingthomas
from sys import version_info
from urllib2 import urlopen
import ssl
from bs4 import BeautifulSoup

#where we attach verse url to get the verse text
verse_text_url = "https://www.openbible.info/labs/cross-references/search?q="

#variable for text input
py3 = False

#gets first verse from user
def get_start_verse():
    py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
    if py3:
        verse = input('Enter verse to start (example: "John 10:10"):\n')
    else:
        verse = raw_input('Enter verse to start (example: "John 10:10"):\n')
    print ""
    #makes it into a verse object and returns it
    return doubtingthomas.make_first_verse(verse)

#gets soup of verse text site
def soup_verse_text(verse):
    url = verse_text_url + verse.url
    ctx = doubtingthomas.verify_false()
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "lxml")
    return soup

#get next reference index from user
def next_ref_index(list_len):
    #get which reference they'd like to see next
    if py3:
        verse_num = input("Type the number of the verse in the list whose cross references you'd like to see, or type 'n' to quit:\n")
    else:
        verse_num = raw_input("Type the number of the verse in the list whose cross references you'd like to see, or type 'n' to quit:\n")

    verse_index = 0

    #check if they tried to quit
    if (verse_num == "n"):
        print "Thanks!"
        return

    #make sure it is a legitimate input
    try:
        verse_index = int(verse_num)
    except ValueError:
        print "Please enter a number in the list\n"
        next_ref_index()

    if (verse_index < 0 or verse_index > list_len):
        print "Please enter a number in the list\n"
        next_ref_index(list_len)
        return

    #if so return it
    return (verse_index - 1)


#gets all crossrefs, displays them and lets you step to the next one if you'd like
def crossref_stepper(verse):
    crossrefs_list = []
    soup = doubtingthomas.soupify(verse)
    crossref_div = soup.find("div", class_="crossrefs")

    if (crossref_div is None):
        print "That verse doesn't exist. Please try again."
        crossref_stepper(get_start_verse())
        return

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

        #gets all cross references, gets their text from another site, saves them into the crossrefs_list
        for ref in hrefs_list:
            refs_list = doubtingthomas.parse_crossref_url(ref)
            for ref in refs_list:
                new_verse = doubtingthomas.Verse(ref)
                new_verse.add_ref_in(verse)
                ref_soup = soup_verse_text(new_verse)
                new_verse.verseText = ref_soup.find("div", class_="crossref-verse").find("p").find(text=True)
                crossrefs_list.append(new_verse)

    #show all crossref options and let user pick the next one
    print "Cross References from " + verse.get_name()
    for idx, ref in enumerate(crossrefs_list):
        print str(idx+1) + ". " + ref.get_name()
        print ref.verseText
        print ""
    verse_index = next_ref_index(len(crossrefs_list))

    if (verse_index is None):
        return

    next_ref = crossrefs_list[verse_index]
    print ""
    crossrefs_list = []
    crossref_stepper(next_ref)
