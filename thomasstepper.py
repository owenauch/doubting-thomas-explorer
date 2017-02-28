import doubtingthomas
from sys import version_info

#gets first verse from user
def get_start_verse():
    py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
    if py3:
        verse = input('Enter verse to start ("John 10:10"):\n')
    else:
        verse = raw_input('Enter verse to start ("John 10:10"):\n')
    return doubtingthomas.make_first_verse(verse)

#gets all crossrefs, displays them and lets you step to the next one if you'd like
def crossref_stepper(verse):
    crossrefs_list = []
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
            new_verse = Verse(ref)
            new_verse.add_ref_in(verse)

#executed code
start_verse = get_start_verse()
crossref_stepper(start_verse)
