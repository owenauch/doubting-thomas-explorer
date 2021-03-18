# Doubting Thomas Explorer:
# A set of scripts to explore the bible through cross references
# thomascsv.py -- uses doubtingthomas.py gathering of verses and formats to csv
#
# Author: Owen Auch
# Matthew 28:17 -- "When they saw him, they worshiped him; but some doubted."

from doubtingthomas import *
import csv
import thomasstepper
from sys import version_info

# creates a csv file with name of your choice and a csv writer
def create_csv(filename):
    myfile = open(filename, 'w')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    return wr

# get max depth from user
def get_max_depth():
    py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
    if py3:
        depth = input("What is the max depth you'd like to go in searching for references?\nLarger numbers take longer -- 10 is usually a good start\n")
    else:
        depth = raw_input("What is the max depth you'd like to go in searching for references?\nLarger numbers take longer -- 10 is usually a good start\n")
    print ("")

    try:
        checked_depth = int(depth)
    except ValueError:
        print ("Please enter a positive number\n")
        get_max_depth()
        return

    return checked_depth

# writes the verses with references in or out underneath
# takes in a csv_writer (wr), verse_list, and a boolean variable
# that's true if it's references out and false if it's references in
def writeRefs(wr, verse_list, if_out):
    which_refs = ""

    if (if_out):
        wr.writerow(["References Out"])
        which_refs = "refsOut"
    else:
        wr.writerow(["References In"])
        which_refs = "refsIn"

    named_verses = []
    refs_list = []
    max_length = 0
    for verse in verse_list:
        named_verses.append(verse.get_name())
        counter = 0
        refs_out_named = []
        for ref in getattr(verse,which_refs):
            counter += 1
            refs_out_named.append(ref.get_name())
        if (counter > max_length):
            max_length = counter
        refs_list.append(refs_out_named)

    wr.writerow(named_verses)

    for sub in refs_list:
        for _ in range(max_length - len(sub)):
            sub.append("")

    refs_zipped = zip(*refs_list)

    for x in refs_zipped:
        wr.writerow(x)

    wr.writerow([""])

# get verse to start and explore through
start_verse = thomasstepper.get_start_verse()
get_next_verses(start_verse, 1, get_max_depth())

#write to csv file "verses.csv"
wr = create_csv("verses.csv")
writeRefs(wr, verse_list, False)
writeRefs(wr, verse_list, True)

