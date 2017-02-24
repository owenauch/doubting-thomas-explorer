from doubtingthomas import *
import csv

myfile = open("test.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
for r in verse_list:
    wr.writerow(r.get_name())
