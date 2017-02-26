from doubtingthomas import *
import csv

# creates a csv file with name of your choice and a csv writer
def create_csv(filename):
    myfile = open(filename, 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    return wr

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

wr = create_csv("test.csv")
writeRefs(wr, verse_list, False)
writeRefs(wr, verse_list, True)
